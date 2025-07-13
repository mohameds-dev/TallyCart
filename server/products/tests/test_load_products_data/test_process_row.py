from products.models import Product
from unittest.mock import patch
from django.test import TestCase
from products.management.commands.load_products_data import Command
from rest_framework import serializers

class ProcessRowTest(TestCase):
    def setUp(self):
        super().setUp()
        self.process_row = Command().process_row
        self.valid_row = {'store_product_id': '30669', 'date': '2/20/2025', 'product_name': 'bananas', 'tags': 'banana fruit', 'unit': 'lb', 'units_per_pack': '3', 'packs_bought': '1', 'sale_price': '$1.49', 'unit_price': '$0.4967', 'store_name': 'Costco Wholesale Pearland  #1221', 'store_location': '3500 Business Center Drive, Pearland TX 77584',}


class ProcessRowProductTest(ProcessRowTest):
    def test_process_row_takes_row_and_calls_serializer(self):
        with patch('products.management.commands.load_products_data.CSVRowSerializer') as mock_serializer:
            mock_serializer.return_value.is_valid.return_value = True
            self.process_row(self.valid_row)

            mock_serializer.assert_called_once_with(data=self.valid_row)
            mock_serializer.return_value.save.assert_called_once()
        
    def test_process_row_raises_exception_if_serializer_is_invalid(self):
        invalid_row = self.valid_row.copy()
        invalid_row.pop('product_name')
        
        with self.assertRaises(serializers.ValidationError):
            self.process_row(invalid_row)

