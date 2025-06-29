from decimal import Decimal
from django.test import TestCase
from products.models import Product, Tag, ProductTag
from shops.models import Shop
from products.serializers import CSVRowSerializer


class LoadProductsDataCommandTest(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name="Test Shop", address="123 Test St")
        self.product = Product.objects.create(name="Test Product", store_product_id="123")
        self.tag = Tag.objects.create(name="sampletag")

    def _get_command_instance(self):
        """Helper method to get a properly initialized command instance."""
        from products.management.commands.load_products_data import Command
        cmd = Command()
        cmd.is_dry_run = False
        cmd.stats = {
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
        return cmd

    # --- CSVRowSerializer Validation Tests ---
    def test_CSVRowSerializer_accepts_valid_complete_data(self):
        data = {
            'store_product_id': 'A1',
            'date': '2/20/2025',
            'product_name': 'Milk',
            'tags': 'dairy fresh',
            'unit': 'liter',
            'units_per_pack': '1',
            'packs_bought': '1',
            'sale_price': '$2.99',
            'unit_price': '$2.99',
            'store_name': 'Shop1',
            'store_location': 'Loc1'
        }
        serializer = CSVRowSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_CSVRowSerializer_extracts_product_name_from_validated_data(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertEqual(serializer.validated_data['product_name'], 'Milk')

    def test_CSVRowSerializer_parses_unit_price_as_decimal(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertEqual(serializer.validated_data['unit_price'], Decimal('2.99'))

    def test_CSVRowSerializer_parses_date_string_to_date_object(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()
        from datetime import date

        self.assertEqual(serializer.validated_data['date'], date(2025, 2, 20))

    def test_CSVRowSerializer_rejects_missing_product_name(self):
        data = {
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_CSVRowSerializer_has_product_name_error_when_missing(self):
        data = {
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertIn('product_name', serializer.errors)

    def test_CSVRowSerializer_rejects_missing_unit_price(self):
        data = {
            'product_name': 'Milk',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_CSVRowSerializer_has_unit_price_error_when_missing(self):
        data = {
            'product_name': 'Milk',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertIn('unit_price', serializer.errors)

    def test_CSVRowSerializer_rejects_invalid_unit_price_format(self):
        data = {
            'product_name': 'Milk',
            'unit_price': 'not_a_number',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_CSVRowSerializer_has_unit_price_error_for_invalid_format(self):
        data = {
            'product_name': 'Milk',
            'unit_price': 'not_a_number',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertIn('unit_price', serializer.errors)

    def test_CSVRowSerializer_rejects_TBD_unit_value(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'TBD',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_CSVRowSerializer_has_unit_error_for_TBD_value(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'TBD',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertIn('unit', serializer.errors)

    def test_CSVRowSerializer_rejects_invalid_date_format(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': '2025-02-20'  # Wrong format
        }
        serializer = CSVRowSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_CSVRowSerializer_has_date_error_for_invalid_format(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': '2025-02-20'  # Wrong format
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertIn('date', serializer.errors)

    def test_CSVRowSerializer_uses_current_date_when_date_is_empty(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$2.99',
            'unit': 'liter',
            'date': ''
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()
        from django.utils import timezone

        self.assertEqual(serializer.validated_data['date'], timezone.now().date())

    def test_CSVRowSerializer_handles_unit_price_with_commas(self):
        data = {
            'product_name': 'Milk',
            'unit_price': '$1,299.99',
            'unit': 'liter',
            'date': '2/20/2025'
        }
        serializer = CSVRowSerializer(data=data)
        serializer.is_valid()

        self.assertEqual(serializer.validated_data['unit_price'], Decimal('1299.99'))

    # --- Tag Processing Tests ---
    def test_process_tags_creates_tag1_for_product(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest1")
        cmd._process_tags_for_product(product, "tag1 tag2 tag3")

        self.assertEqual(ProductTag.objects.filter(product=product, tag__name="tag1").count(), 1)

    def test_process_tags_creates_tag2_for_product(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest2")
        cmd._process_tags_for_product(product, "tag1 tag2 tag3")

        self.assertEqual(ProductTag.objects.filter(product=product, tag__name="tag2").count(), 1)

    def test_process_tags_creates_tag3_for_product(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest3")
        cmd._process_tags_for_product(product, "tag1 tag2 tag3")

        self.assertEqual(ProductTag.objects.filter(product=product, tag__name="tag3").count(), 1)

    def test_process_tags_handles_empty_tag_string(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest4")
        cmd._process_tags_for_product(product, "")

        self.assertEqual(ProductTag.objects.filter(product=product).count(), 0)

    # --- Shop Creation Tests ---
    def test_get_or_create_shop_returns_shop_instance_for_new_shop(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop', 'store_location': 'New Loc'}
        shop = cmd._get_or_create_shop(data)

        self.assertIsInstance(shop, Shop)

    def test_get_or_create_shop_sets_correct_name_for_new_shop(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop2', 'store_location': 'New Loc2'}
        shop = cmd._get_or_create_shop(data)

        self.assertEqual(shop.name, 'New Shop2')

    def test_get_or_create_shop_sets_correct_address_for_new_shop(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop3', 'store_location': 'New Loc3'}
        shop = cmd._get_or_create_shop(data)

        self.assertEqual(shop.address, 'New Loc3')

    def test_get_or_create_shop_increments_created_stats_for_new_shop(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop4', 'store_location': 'New Loc4'}
        cmd._get_or_create_shop(data)

        self.assertEqual(cmd.stats['shops_created'], 1)

    def test_get_or_create_shop_returns_existing_shop_instance(self):
        cmd = self._get_command_instance()
        existing_shop = Shop.objects.create(name="Existing Shop", address="Existing Loc")
        data = {'store_name': 'Existing Shop', 'store_location': 'Existing Loc'}
        shop = cmd._get_or_create_shop(data)

        self.assertEqual(shop, existing_shop)

    def test_get_or_create_shop_increments_skipped_stats_for_existing_shop(self):
        cmd = self._get_command_instance()
        Shop.objects.create(name="Existing Shop2", address="Existing Loc2")
        data = {'store_name': 'Existing Shop2', 'store_location': 'Existing Loc2'}
        cmd._get_or_create_shop(data)

        self.assertEqual(cmd.stats['shops_skipped'], 1)

    # --- Product Creation Tests ---
    def test_get_or_create_product_returns_product_instance_for_new_product(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product', 'store_product_id': 'NP1'}
        product = cmd._get_or_create_product(data)

        self.assertIsInstance(product, Product)

    def test_get_or_create_product_sets_correct_name_for_new_product(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product2', 'store_product_id': 'NP2'}
        product = cmd._get_or_create_product(data)

        self.assertEqual(product.name, 'New Product2')

    def test_get_or_create_product_sets_correct_store_product_id_for_new_product(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product3', 'store_product_id': 'NP3'}
        product = cmd._get_or_create_product(data)

        self.assertEqual(product.store_product_id, 'NP3')

    def test_get_or_create_product_increments_created_stats_for_new_product(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product4', 'store_product_id': 'NP4'}
        cmd._get_or_create_product(data)

        self.assertEqual(cmd.stats['products_created'], 1)

    def test_get_or_create_product_returns_existing_product_instance(self):
        cmd = self._get_command_instance()
        existing_product = Product.objects.create(name="Existing Product", store_product_id="EP1")
        data = {'product_name': 'Existing Product', 'store_product_id': 'EP1'}
        product = cmd._get_or_create_product(data)

        self.assertEqual(product, existing_product)

    def test_get_or_create_product_increments_skipped_stats_for_existing_product(self):
        cmd = self._get_command_instance()
        Product.objects.create(name="Existing Product2", store_product_id="EP2")
        data = {'product_name': 'Existing Product2', 'store_product_id': 'EP2'}
        cmd._get_or_create_product(data)

        self.assertEqual(cmd.stats['products_skipped'], 1)

# TODO: Add tests for price snapshot creation
