import os
import csv
from django.core.management.base import BaseCommand, CommandError
from products.serializers import CSVRowSerializer

class Command(BaseCommand):
    
    help = 'Load products data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing products data'
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'CSV file not found: {csv_file_path}')


        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row_index, row_data in enumerate(reader, start=2):
                try:
                    self.process_row(row_data)
                    self.stdout.write(f'Processed row {row_index}.')
                except Exception as e:
                    self.stderr.write(f'Skipped row {row_index}: {e}')

        print('Done! Here are the counts of the records in the db:')
        from products.models import Product, PriceSnapshot, Shop, Tag
        print(f'Products: {Product.objects.count()}')
        print(f'PriceSnapshots: {PriceSnapshot.objects.count()}')
        print(f'Shops: {Shop.objects.count()}')
        print(f'Tags: {Tag.objects.count()}')

    def process_row(self, row):
        row['source'] = 'CSV input'
        serializer = CSVRowSerializer(data=row)
        serializer.is_valid(raise_exception=True)
        serializer.save()
