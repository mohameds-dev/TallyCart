import csv
import os
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime
from products.models import Product, PriceSnapshot
from shops.models import Shop


class Command(BaseCommand):
    """
    Loads product and price data from a CSV file into the database.

    This command processes a CSV file to create or update products, shops,
    and price snapshots. It's designed to be robust, handling various
    data cleaning and validation tasks before committing to the database.

    The process is separated into two main phases for each row:
    1.  **Validation and Cleaning**: Each row is validated for essential data
        and cleaned (e.g., parsing dates and decimals).
    2.  **Database Loading**: Validated data is used to create or retrieve
        database records.

    This separation ensures that the database logic is clean and operates on
    predictable data, making the process more testable and maintainable.
    """
    help = 'Load products data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing products data'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating records'
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.is_dry_run = options['dry_run']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'CSV file not found: {csv_file_path}')

        if self.is_dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No records will be created'))

        stats = {
            'products_created': 0,
            'products_skipped': 0,
            'shops_created': 0,
            'shops_skipped': 0,
            'price_snapshots_created': 0,
            'price_snapshots_skipped': 0,
            'skipped_missing_data': 0,
            'skipped_invalid': 0,
            'skipped_duplicate_snapshot': 0,
            'errors': 0
        }

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                cleaned_data = self._filter_and_clean_data(reader, stats)
                
                self.stdout.write(f"Finished filtering. Found {len(cleaned_data)} valid rows to process.")
                
                self._load_data_to_db(cleaned_data, stats)

        except Exception as e:
            raise CommandError(f'An unexpected error occurred: {e}')

        self._print_summary(stats, self.is_dry_run)

    def _filter_and_clean_data(self, reader, stats):
        """
        Reads the CSV, validates and cleans each row, and returns a list of clean data.
        """
        cleaned_data = []
        for row_num, row in enumerate(reader, start=2):
            try:
                cleaned_row, skip_reason = self._clean_and_validate_row(row, row_num)
                if cleaned_row:
                    cleaned_data.append(cleaned_row)
                else:
                    stats[f'skipped_{skip_reason}'] += 1
            except (ValueError, InvalidOperation) as e:
                stats['skipped_invalid'] += 1
                self.stdout.write(self.style.ERROR(f"Skipping row {row_num} due to invalid data: {e}"))
        return cleaned_data

    def _clean_and_validate_row(self, row, row_num):
        """
        Validates a single row, parses its data, and returns a structured dictionary and skip reason.
        Prints details if the row is invalid or missing data.
        """
        required_fields = ['item_name', 'unit_price']
        missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
        item_name = row.get('item_name', '').strip()
        unit_price_str = row.get('unit_price', '').strip()

        if missing_fields:
            self.stdout.write(self.style.WARNING(
                f"Skipping row {row_num}: missing data in fields {missing_fields}\nRow content: {row}"
            ))
            return None, 'missing_data'

        try:
            unit_price = Decimal(unit_price_str.replace('$', '').replace(',', ''))
        except Exception:
            self.stdout.write(self.style.WARNING(
                f"Skipping row {row_num}: invalid unit_price value '{unit_price_str}'\nRow content: {row}"
            ))
            return None, 'invalid'
        
        date_str = row.get('date', '').strip()
        try:
            snapshot_date = self._parse_date(date_str)
        except Exception:
            self.stdout.write(self.style.WARNING(
                f"Skipping row {row_num}: invalid date value '{date_str}'\nRow content: {row}"
            ))
            return None, 'invalid'

        return ({
            'item_name': item_name,
            'store_item_id': row.get('store_item_id', '').strip(),
            'store_name': row.get('store_name', '').strip(),
            'store_location': row.get('store_location', '').strip(),
            'date': snapshot_date,
            'unit': row.get('unit', 'unit').strip(),
            'unit_price': unit_price
        }, None)

    def _parse_date(self, date_str):
        """Parses a date string, only accepting the format m/d/Y (e.g., 2/20/2025)."""
        if not date_str:
            return timezone.now().date()
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            raise ValueError(f"Date format for '{date_str}' not recognized. Expected m/d/Y (e.g., 2/20/2025)")

    def _load_data_to_db(self, cleaned_data, stats):
        """
        Loads the cleaned data into the database.
        """
        for row_num, data_row in enumerate(cleaned_data, start=1):
            try:
                shop = self._get_or_create_shop(data_row, stats)
                product = self._get_or_create_product(data_row, stats)
                self._create_price_snapshot(product, shop, data_row, stats)
                
                if row_num % 100 == 0:
                    self.stdout.write(f'Processed {row_num}/{len(cleaned_data)} rows...')
            except Exception as e:
                stats['errors'] += 1
                self.stdout.write(self.style.ERROR(f'Error loading data row {row_num}: {e}'))

    def _get_or_create_shop(self, data, stats):
        """Gets or creates a Shop, returning None if no name is provided."""
        store_name = data['store_name']
        if not store_name:
            return None
        
        try:
            shop = Shop.objects.get(name=store_name)
            stats['shops_skipped'] += 1
            return shop
        except Shop.DoesNotExist:
            shop = self._create_object(Shop, name=store_name, address=data['store_location'] or None)
            stats['shops_created'] += 1
            return shop

    def _get_or_create_product(self, data, stats):
        """Gets or creates a Product."""
        try:
            product = Product.objects.get(name=data['item_name'])
            stats['products_skipped'] += 1
        except Product.DoesNotExist:
            product = self._create_object(
                Product,
                name=data['item_name'],
                store_product_id=data['store_item_id'] or None
            )
            stats['products_created'] += 1
        return product

    def _create_price_snapshot(self, product, shop, data, stats):
        """Creates a PriceSnapshot, skipping duplicates."""
        snapshot_exists = PriceSnapshot.objects.filter(
            product=product,
            shop=shop,
            date=data['date'],
            unit=data['unit']
        ).exists()

        if snapshot_exists:
            stats['skipped_duplicate_snapshot'] += 1
            return

        self._create_object(
            PriceSnapshot,
            product=product,
            shop=shop,
            date=data['date'],
            unit=data['unit'],
            unit_price=data['unit_price'],
            currency='USD',
            source='csv_import'
        )
        stats['price_snapshots_created'] += 1

    def _create_object(self, model, **kwargs):
        """
        Helper to create a model instance, either in-memory (dry run) or in the DB.
        """
        if self.is_dry_run:
            return model(**kwargs)
        else:
            return model.objects.create(**kwargs)

    def _print_summary(self, stats, is_dry_run):
        """Prints a summary of the import operation."""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('IMPORT SUMMARY')
        self.stdout.write('='*50)
        
        if is_dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No records were actually created'))
            
        self.stdout.write(f"Shops: {stats['shops_created']} created, {stats['shops_skipped']} skipped")
        self.stdout.write(f"Products: {stats['products_created']} created, {stats['products_skipped']} skipped")
        self.stdout.write(f"Price Snapshots: {stats['price_snapshots_created']} created, {stats['skipped_duplicate_snapshot']} skipped (duplicate), {stats['price_snapshots_skipped']} skipped (other)")
        self.stdout.write(f"Rows skipped (missing data): {stats['skipped_missing_data']}")
        self.stdout.write(f"Rows skipped (invalid data): {stats['skipped_invalid']}")
        
        if stats['errors'] > 0:
            self.stdout.write(self.style.ERROR(f"Errors during DB load: {stats['errors']}"))
        else:
            self.stdout.write(self.style.SUCCESS("No errors encountered during DB load."))
            
        self.stdout.write('='*50) 
