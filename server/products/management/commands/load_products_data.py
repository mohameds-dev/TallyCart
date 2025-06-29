import csv
import os
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime
from products.models import Product, PriceSnapshot
from shops.models import Shop
from products.models import Tag


class Command(BaseCommand):
    """
    Loads product and price data from a CSV file into the database.

    This command processes a CSV file to create or update products, shops,
    and price snapshots. It's designed to be robust, handling various
    data cleaning and validation tasks before committing to the database.

    The process is separated into two main phases for each row:
    1.  **Validation and Cleaning**: Each row is validated for essential data
        and cleaned (e.g., parsing dates and decimals).
    2.  **Database Loading**: Validated data is used to create or update
        database records.
    """
    help = 'Load products data from a CSV file into the database'

    CSV_FIELD_MAP = {
        'product_name': 'product_name',
        'store_product_id': 'store_product_id',
        'store_name': 'store_name',
        'store_location': 'store_location',
        'date': 'date',
        'unit': 'unit',
        'unit_price': 'unit_price',
        'tags': 'tags',
    }

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

        self.stats = {
            'products_created': 0,
            'products_skipped': 0,
            'products_skipped_missing_data': 0,
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
                
                cleaned_data = self._filter_and_clean_data(reader)
                
                self.stdout.write(f"Finished filtering. Found {len(cleaned_data)} valid rows to process.")
                
                self._load_data_to_db(cleaned_data)

        except Exception as e:
            raise CommandError(f'An unexpected error occurred: {e}')

        self._print_summary(self.is_dry_run)

    def _filter_and_clean_data(self, reader):
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
                    self.stats[f'skipped_{skip_reason}'] += 1
            except (ValueError, InvalidOperation) as e:
                self.stats['skipped_invalid'] += 1
                self.stdout.write(self.style.ERROR(f"Skipping row {row_num} due to invalid data: {e}"))
        return cleaned_data

    def _clean_and_validate_row(self, row, row_num):
        """
        Validates a single row, parses its data, and returns a structured dictionary and skip reason.
        Prints details if the row is invalid or missing data.
        """
        field_map = self.CSV_FIELD_MAP
        required_fields = ['product_name', 'unit_price']
        missing_fields = [field for field in required_fields if not row.get(field_map[field], '').strip()]
        product_name = row.get(field_map['product_name'], '').strip()
        unit_price_str = row.get(field_map['unit_price'], '').strip()
        unit_value = row.get(field_map['unit'], 'unit').strip()
        tags_string = row.get(field_map['tags'], '').strip()

        if missing_fields:
            self.stdout.write(self.style.WARNING(
                f"Skipping row {row_num}: missing data in fields {missing_fields}\nRow content: {str(row)[:70]}..."
            ))
            return ({'skip_product': True}, 'missing_data')

        if unit_value.lower() == 'tbd':
            self.stdout.write(self.style.WARNING(
                f"Skipping row {row_num}: unit is 'TBD' (data not filled)\nRow content: {str(row)[:70]}..."
            ))
            return ({'skip_product': True}, 'missing_data')

        try:
            unit_price = Decimal(unit_price_str.replace('$', '').replace(',', ''))
        except Exception:
            self.stdout.write(self.style.WARNING(
                f"Skipping row {row_num}: invalid unit_price value '{unit_price_str}'\nRow content: {str(row)[:70]}..."
            ))
            return None, 'invalid'
        
        date_str = row.get(field_map['date'], '').strip()
        try:
            snapshot_date = self._parse_date(date_str)
        except Exception:
            self.stdout.write(self.style.WARNING(
                f"Skipping row {row_num}: invalid date value '{date_str}'\nRow content: {str(row)[:70]}..."
            ))
            return None, 'invalid'

        return ({
            'product_name': product_name,
            'store_product_id': row.get(field_map['store_product_id'], '').strip(),
            'store_name': row.get(field_map['store_name'], '').strip(),
            'store_location': row.get(field_map['store_location'], '').strip(),
            'date': snapshot_date,
            'unit': unit_value,
            'unit_price': unit_price,
            'tags': tags_string,
        }, None)

    def _parse_date(self, date_str):
        """Parses a date string, only accepting the format m/d/Y (e.g., 2/20/2025)."""
        if not date_str:
            return timezone.now().date()
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            raise ValueError(f"Date format for '{date_str}' not recognized. Expected m/d/Y (e.g., 2/20/2025)")

    def _load_data_to_db(self, cleaned_data):
        """
        Loads the cleaned data into the database.
        """
        for row_num, data_row in enumerate(cleaned_data, start=1):
            try:
                if data_row.get('skip_product'):
                    self.stats['products_skipped_missing_data'] += 1
                    continue
                shop = self._get_or_create_shop(data_row)
                product = self._get_or_create_product(data_row)
                self._process_tags_for_product(product, data_row.get('tags', ''))
                self._create_price_snapshot(product, shop, data_row)
                
                if row_num % 100 == 0:
                    self.stdout.write(f'Processed {row_num}/{len(cleaned_data)} rows...')
            except Exception as e:
                self.stats['errors'] += 1
                self.stdout.write(self.style.ERROR(f'Error loading data row {row_num}: {e}'))

    def _get_or_create_shop(self, data):
        """Gets or creates a Shop, returning None if no name is provided."""
        store_name = data['store_name']
        if not store_name:
            return None
        
        try:
            shop = Shop.objects.get(name=store_name)
            self.stats['shops_skipped'] += 1
            return shop
        except Shop.DoesNotExist:
            shop = self._create_object(Shop, name=store_name, address=data['store_location'] or None)
            self.stats['shops_created'] += 1
            return shop

    def _get_or_create_product(self, data):
        """Gets or creates a Product."""
        try:
            product = Product.objects.get(name=data['product_name'])
            self.stats['products_skipped'] += 1
        except Product.DoesNotExist:
            product = self._create_object(
                Product,
                name=data['product_name'],
                store_product_id=data['store_product_id'] or None
            )
            self.stats['products_created'] += 1
        return product

    def _create_price_snapshot(self, product, shop, data):
        """Creates a PriceSnapshot, skipping duplicates."""
        snapshot_exists = PriceSnapshot.objects.filter(
            product=product,
            shop=shop,
            date=data['date'],
            unit=data['unit']
        ).exists()

        if snapshot_exists:
            self.stats['skipped_duplicate_snapshot'] += 1
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
        self.stats['price_snapshots_created'] += 1

    def _process_tags_for_product(self, product, tags_string):
        """Process and assign tags to the product from a space-separated string."""
        if not tags_string:
            return
        tag_names = [tag.strip().lower() for tag in tags_string.split() if tag.strip()]
        for tag_name in tag_names:
            # Skip empty tags
            if not tag_name:
                continue
            tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
            product.tags.add(tag_obj)

    def _create_object(self, model, **kwargs):
        """
        Helper to create a model instance, either in-memory (dry run) or in the DB.
        """
        if self.is_dry_run:
            return model(**kwargs)
        else:
            return model.objects.create(**kwargs)

    def _print_summary(self, is_dry_run):
        """Prints a summary of the import operation."""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('IMPORT SUMMARY')
        self.stdout.write('='*50)
        
        if is_dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No records were actually created'))
            
        self.stdout.write(f"Shops: {self.stats['shops_created']} created, {self.stats['shops_skipped']} skipped")
        self.stdout.write(f"Products: {self.stats['products_created']} created, {self.stats['products_skipped']} skipped, {self.stats['products_skipped_missing_data']} skipped (missing data)")
        self.stdout.write(f"Price Snapshots: {self.stats['price_snapshots_created']} created, {self.stats['skipped_duplicate_snapshot']} skipped (duplicate), {self.stats['price_snapshots_skipped']} skipped (other)")
        self.stdout.write(f"Rows skipped (missing data): {self.stats['skipped_missing_data']}")
        self.stdout.write(f"Rows skipped (invalid data): {self.stats['skipped_invalid']}")
        
        if self.stats['errors'] > 0:
            self.stdout.write(self.style.ERROR(f"Errors during DB load: {self.stats['errors']}"))
        else:
            self.stdout.write(self.style.SUCCESS("No errors encountered during DB load."))
            
        self.stdout.write('='*50) 
