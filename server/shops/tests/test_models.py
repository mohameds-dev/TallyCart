from django.test import TestCase
from shops.models import Shop
from decimal import Decimal


class ShopModelTests(TestCase):
    def test_shop_str_name_representation_correctness(self):
        shop = Shop.objects.create(name="Test Shop")
        self.assertEqual(str(shop), "Test Shop")

    def test_shop_field_initialization_correctness(self):
        shop_data = {
            "name": "Test Shop",
            "address": "123 Main St, Anytown, USA",
            "url": "https://www.testshop.com",
            "latitude": Decimal('12.34567890'),
            "longitude": Decimal('78.90123456')
        }
        shop = Shop.objects.create(**shop_data)
        
        self.assertEqual(shop_data, {
            "name": shop.name,
            "address": shop.address,
            "url": shop.url,
            "latitude": shop.latitude,
            "longitude": shop.longitude
        })

    def test_shop_default_values_correctness(self):
        shop = Shop.objects.create(name="Test Shop")
        record_data = {
            "name": shop.name,
            "address": shop.address,
            "url": shop.url,
            "latitude": shop.latitude,
            "longitude": shop.longitude
        }

        self.assertEqual(record_data, {
            "name": "Test Shop",
            "address": "",
            "url": "",
            "latitude": None,
            "longitude": None
        })


    def test_shop_str_name_representation_correctness_with_address(self):
        shop = Shop.objects.create(name="Test Shop", address="123 Main St, Anytown, USA")
        self.assertEqual(str(shop), "Test Shop AT 123 Main St, Anytown, USA")

    def test_shop_str_name_representation_correctness_with_address_and_url(self):
        shop = Shop.objects.create(name="Test Shop", address="123 Main St, Anytown, USA", url="https://www.testshop.com")
        self.assertEqual(str(shop), "Test Shop AT 123 Main St, Anytown, USA - https://www.testshop.com")
