from django.test import TestCase
from products.serializers import CSVRowSerializer
from rest_framework import serializers
from products.models import Product

class CSVRowSerializerTest(TestCase):
    def setUp(self):
        self.valid_row = {'store_product_id': '30669', 'date': '2/20/2025', 'product_name': 'bananas', 'tags': 'banana fruit multiple_words_tag', 'unit': 'lb', 'units_per_pack': '3', 'packs_bought': '1', 'sale_price': '$1.49', 'unit_price': '$0.4967', 'store_name': 'Costco Wholesale Pearland  #1221', 'store_location': '3500 Business Center Drive, Pearland TX 77584',}

    def test_serializer_validates_valid_row(self):
        serializer = CSVRowSerializer(data=self.valid_row)

        self.assertTrue(serializer.is_valid())

    def test_serializer_raises_exception_if_row_is_invalid(self):
        invalid_row = self.valid_row.copy()
        invalid_row.pop('product_name')

        with self.assertRaises(serializers.ValidationError):
            serializer = CSVRowSerializer(data=invalid_row)
            serializer.is_valid(raise_exception=True)

    def test_serializer_takes_a_valid_row_and_creates_a_new_product(self):
        serializer = CSVRowSerializer(data=self.valid_row)
        if serializer.is_valid():
            serializer.save()

        self.assertEqual(Product.objects.count(), 1)

    def test_serializer_takes_a_valid_row_and_creates_a_new_product_with_valid_name(self):
        serializer = CSVRowSerializer(data=self.valid_row)
        if serializer.is_valid():
            serializer.save()
        product = Product.objects.get(name=self.valid_row['product_name'])

        self.assertEqual(product.name, self.valid_row['product_name'])

    def test_serializer_takes_a_valid_row_and_creates_a_product_with_two_tags(self):
        serializer = CSVRowSerializer(data=self.valid_row)
        if serializer.is_valid():
            serializer.save()
        product = Product.objects.get(name=self.valid_row['product_name'])

        self.assertEqual(product.tags.count(), 3)

    def test_serializer_takes_a_valid_row_and_creates_a_product_with_two_correct_tags(self):
        serializer = CSVRowSerializer(data=self.valid_row)
        if serializer.is_valid():
            serializer.save()
        product = Product.objects.get(name=self.valid_row['product_name'])
        tags = product.tags.all()

        self.assertEqual([tag.name for tag in tags], self.valid_row['tags'].split())


    
        

