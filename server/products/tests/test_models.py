from django.test import TestCase
from products.models import Product, Tag, ProductTag, PriceSnapshot
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from shops.models import Shop
from datetime import date

class ProductModelTests(TestCase):
    def test_canary(self):
        self.assertTrue(True)

    def test_product_name_uniqueness(self):
        Product.objects.create(name="Test Product")
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="Test Product")

    def test_product_name_exceeding_max_length_raises_validation_error_with_full_clean_and_save(self):
        product = Product(name="A" * 256)
        with self.assertRaises(ValidationError):
            product.full_clean()
            product.save()
    
    def test_product_str_representation(self):
        product = Product.objects.create(name="Test Product")
        self.assertEqual(str(product), "Test Product")

    def test_long_product_name_truncation(self):
        long_name = "This is a very long product name that should be truncated..."
        product = Product.objects.create(name=long_name)
        self.assertEqual(str(product), f"{long_name[:50]}")


class ProductTagModelTests(TestCase):
    def test_tag_str_representation_correctness(self):
        tag = Tag.objects.create(name="Test Tag")
        self.assertEqual(str(tag), "Test Tag")

    def test_product_tag_str_representation_correctness(self):
        product = Product.objects.create(name="Test Product")
        tag = Tag.objects.create(name="Test Tag")
        product_tag = ProductTag.objects.create(product=product, tag=tag)
        self.assertEqual(str(product_tag), f"{product} - TAGGED: {tag}")

    def test_product_tag_unique_together_constraint_prevents_duplicate_tags_on_same_product(self):
        product = Product.objects.create(name="Test Product")
        tag = Tag.objects.create(name="Test Tag")
        ProductTag.objects.create(product=product, tag=tag)
        with self.assertRaises(IntegrityError):
            ProductTag.objects.create(product=product, tag=tag)

    def test_count_multiple_tags_for_product_correctness(self):
        product = Product.objects.create(name="Test Product")
        tag1 = Tag.objects.create(name="Test Tag 1")
        tag2 = Tag.objects.create(name="Test Tag 2")
        ProductTag.objects.create(product=product, tag=tag1)
        ProductTag.objects.create(product=product, tag=tag2)
        self.assertEqual(product.tags.count(), 2)

    def test_retrieving_products_by_tag(self):
        product1 = Product.objects.create(name="Product 1")
        product2 = Product.objects.create(name="Product 2")
        tag = Tag.objects.create(name="Test Tag")
        ProductTag.objects.create(product=product1, tag=tag)
        ProductTag.objects.create(product=product2, tag=tag)
        products = Product.objects.filter(tags=tag)
        
        self.assertEqual(list(products), [product1, product2])


class PriceSnapshotModelTests(TestCase):
    def test_price_snapshot_str_representation_correctness(self):
        product = Product.objects.create(name="Test Product")
        shop = Shop.objects.create(name="Test Shop")
        price_snapshot = PriceSnapshot.objects.create(product=product, shop=shop, unit_price=100)
        
        self.assertEqual(str(price_snapshot), f"{product} - FOR 100.00 USD / unit - ON {price_snapshot.date} FROM {shop}")

    def test_price_snapshot_unique_together_constraint_prevents_duplicate_price_snapshots_for_same_product_and_shop(self):
        product = Product.objects.create(name="Test Product")
        shop = Shop.objects.create(name="Test Shop")
        PriceSnapshot.objects.create(product=product, shop=shop, unit_price=100)

        with self.assertRaises(IntegrityError):
            PriceSnapshot.objects.create(product=product, shop=shop, unit_price=100)

    def test_price_snapshot_retrieves_records_ordered_by_most_recent(self):
        product1 = Product.objects.create(name="Test Product 1")
        product2 = Product.objects.create(name="Test Product 2")
        shop = Shop.objects.create(name="Test Shop")
        PriceSnapshot.objects.create(product=product1, shop=shop, unit_price=100, date=date(2021, 1, 1))
        PriceSnapshot.objects.create(product=product2, shop=shop, unit_price=200, date=date(2021, 1, 2))

        self.assertEqual(list(PriceSnapshot.objects.all()), [
            PriceSnapshot.objects.get(unit_price=200),
            PriceSnapshot.objects.get(unit_price=100),
        ]) 