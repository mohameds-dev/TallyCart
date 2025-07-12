from django.test import TestCase
from products.management.commands.load_products_data import Command
from unittest.mock import patch
from products.models import Product

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
        with patch('products.management.commands.load_products_data.CSVRowSerializer') as mock_serializer:
            mock_serializer.return_value.is_valid.return_value = False
            invalid_row = self.valid_row.copy()
            invalid_row.pop('product_name')
            
            with self.assertRaises(ValueError):
                self.process_row(invalid_row)
        
    def test_process_row_takes_valid_row_and_a_new_product_is_created(self):
        self.process_row(self.valid_row)

        self.assertEqual(Product.objects.count(), 1)

    def test_process_row_takes_valid_row_and_a_new_product_is_created_with_valid_name(self):
        self.process_row(self.valid_row)

        product = Product.objects.get(name=self.valid_row['product_name'])
        self.assertEqual(product.name, self.valid_row['product_name'])

class ProcessRowTagTest(ProcessRowTest):
    def test_process_row_takes_valid_row_and_a_new_product_is_created_with_two_tags(self):
        self.process_row(self.valid_row)

        product = Product.objects.get(name=self.valid_row['product_name'])
        self.assertEqual(product.tags.count(), 2)

    def test_process_row_takes_valid_row_and_a_new_product_is_created_with_the_two_correct_tags(self):
        self.process_row(self.valid_row)
        product = Product.objects.get(name=self.valid_row['product_name'])
        tags = product.tags.all()
        valid_tags_names = self.valid_row['tags'].split(' ')

        self.assertEqual([tag.name for tag in tags], valid_tags_names)


class ProcessRowStorePriceTest(ProcessRowTest):
    pass
