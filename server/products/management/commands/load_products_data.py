import csv
from django.core.management.base import BaseCommand
from products.csv_utils import resolve_csv_path
from products.serializers import CSVRowSerializer


class Command(BaseCommand):
    help = 'Load products data from a CSV file. If no path is provided, downloads the default CSV from Google Sheets.'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            nargs='?',
            default=None,
            help='Path to local CSV file. If not provided, downloads default CSV from Google Sheets.'
        )

    def handle(self, *args, **options):
        csv_path = options['csv_file']
        
        if csv_path is None:
            self.stdout.write('Downloading default CSV...')
        
        file_path = resolve_csv_path(csv_path)
        self._load_csv(file_path)
        self._print_summary()

    def _load_csv(self, file_path):
        """Load and process CSV file."""
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row_index, row_data in enumerate(reader, start=2):
                try:
                    self._process_row(row_data)
                    self.stdout.write(f'Processed row {row_index}.')
                except Exception as e:
                    self.stderr.write(f'Skipped row {row_index}: {e}')

    def _process_row(self, row):
        """Process a single CSV row."""
        row['source'] = 'CSV input'
        serializer = CSVRowSerializer(data=row)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def _print_summary(self):
        """Print summary of loaded data."""
        self.stdout.write('Done! Here are the counts of the records in the db:')
        from products.models import Product, PriceSnapshot, Shop, Tag
        self.stdout.write(f'Products: {Product.objects.count()}')
        self.stdout.write(f'PriceSnapshots: {PriceSnapshot.objects.count()}')
        self.stdout.write(f'Shops: {Shop.objects.count()}')
        self.stdout.write(f'Tags: {Tag.objects.count()}')
