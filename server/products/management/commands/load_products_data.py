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
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating records'
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        # self.is_dry_run = options['dry_run']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'CSV file not found: {csv_file_path}')

        # if self.is_dry_run:
        #     self.stdout.write(self.style.WARNING('DRY RUN MODE - No records will be created'))

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            # print(reader.fieldnames)
            row_index = 2
            for row in enumerate(reader, start=row_index):
                try:
                    self.process_row(row)
                    row_index += 1
                except Exception as e:
                    self.stderr.write(f'Skipping row {row_index}: {e}')

    def process_row(self, row):
        serializer = CSVRowSerializer(data=row)
        if serializer.is_valid():
            serializer.save()
        else:
           raise ValueError(serializer.errors)
                

    