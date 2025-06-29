from decimal import Decimal
from django.test import TestCase
from products.models import Product, Tag, ProductTag
from shops.models import Shop

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

    # --- Clean and Validate Row ---
    def test_clean_and_validate_row_valid_not_none(self):
        cmd = self._get_command_instance()
        row = {
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
        cleaned, reason = cmd._clean_and_validate_row(row, 1)

        self.assertIsNotNone(cleaned)

    def test_clean_and_validate_row_valid_reason_none(self):
        cmd = self._get_command_instance()
        row = {
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
        cleaned, reason = cmd._clean_and_validate_row(row, 1)

        self.assertIsNone(reason)

    def test_clean_and_validate_row_valid_product_name(self):
        cmd = self._get_command_instance()
        row = {
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
        cleaned, _ = cmd._clean_and_validate_row(row, 1)

        self.assertEqual(cleaned['product_name'], 'Milk')

    def test_clean_and_validate_row_valid_unit_price(self):
        cmd = self._get_command_instance()
        row = {
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
        cleaned, _ = cmd._clean_and_validate_row(row, 1)

        self.assertEqual(cleaned['unit_price'], Decimal('2.99'))

    def test_clean_and_validate_row_missing_data_skip(self):
        cmd = self._get_command_instance()
        row = {
            'store_product_id': 'A1',
            'date': '2/20/2025',
            'product_name': '',
            'tags': 'dairy fresh',
            'unit': 'liter',
            'units_per_pack': '1',
            'packs_bought': '1',
            'sale_price': '$2.99',
            'unit_price': '',
            'store_name': 'Shop1',
            'store_location': 'Loc1'
        }
        cleaned, reason = cmd._clean_and_validate_row(row, 1)

        self.assertTrue(cleaned['skip_product'])

    def test_clean_and_validate_row_missing_data_reason(self):
        cmd = self._get_command_instance()
        row = {
            'store_product_id': 'A1',
            'date': '2/20/2025',
            'product_name': '',
            'tags': 'dairy fresh',
            'unit': 'liter',
            'units_per_pack': '1',
            'packs_bought': '1',
            'sale_price': '$2.99',
            'unit_price': '',
            'store_name': 'Shop1',
            'store_location': 'Loc1'
        }
        _, reason = cmd._clean_and_validate_row(row, 1)

        self.assertEqual(reason, 'missing_data')

    def test_clean_and_validate_row_TBD_unit_skip(self):
        cmd = self._get_command_instance()
        row = {
            'store_product_id': 'A1',
            'date': '2/20/2025',
            'product_name': 'Milk',
            'tags': 'dairy fresh',
            'unit': 'TBD',
            'units_per_pack': '1',
            'packs_bought': '1',
            'sale_price': '$2.99',
            'unit_price': '$2.99',
            'store_name': 'Shop1',
            'store_location': 'Loc1'
        }
        cleaned, reason = cmd._clean_and_validate_row(row, 1)

        self.assertTrue(cleaned['skip_product'])

    def test_clean_and_validate_row_TBD_unit_reason(self):
        cmd = self._get_command_instance()
        row = {
            'store_product_id': 'A1',
            'date': '2/20/2025',
            'product_name': 'Milk',
            'tags': 'dairy fresh',
            'unit': 'TBD',
            'units_per_pack': '1',
            'packs_bought': '1',
            'sale_price': '$2.99',
            'unit_price': '$2.99',
            'store_name': 'Shop1',
            'store_location': 'Loc1'
        }
        _, reason = cmd._clean_and_validate_row(row, 1)

        self.assertEqual(reason, 'missing_data')

    # --- Date Parsing ---
    def test_parse_date_valid_1(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()

        self.assertEqual(str(cmd._parse_date('2/20/2025')), '2025-02-20')

    def test_parse_date_valid_2(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()

        self.assertEqual(str(cmd._parse_date('8/13/2024')), '2024-08-13')

    def test_parse_date_invalid(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()

        with self.assertRaises(ValueError):
            cmd._parse_date('2025-02-20')

    def test_parse_date_empty(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        from django.utils import timezone
        result = cmd._parse_date('')

        self.assertEqual(result, timezone.now().date())

    # --- Tag Processing ---
    def test_process_tags_for_product_tag1(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest1")
        cmd._process_tags_for_product(product, "tag1 tag2 tag3")

        self.assertEqual(ProductTag.objects.filter(product=product, tag__name="tag1").count(), 1)

    def test_process_tags_for_product_tag2(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest2")
        cmd._process_tags_for_product(product, "tag1 tag2 tag3")

        self.assertEqual(ProductTag.objects.filter(product=product, tag__name="tag2").count(), 1)

    def test_process_tags_for_product_tag3(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest3")
        cmd._process_tags_for_product(product, "tag1 tag2 tag3")

        self.assertEqual(ProductTag.objects.filter(product=product, tag__name="tag3").count(), 1)

    def test_process_tags_empty(self):
        from products.management.commands.load_products_data import Command
        cmd = Command()
        product = Product.objects.create(name="TagTest4")
        cmd._process_tags_for_product(product, "")

        self.assertEqual(ProductTag.objects.filter(product=product).count(), 0)

    # --- Shop/Product Creation ---
    def test_get_or_create_shop_new_instance(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop', 'store_location': 'New Loc'}
        shop = cmd._get_or_create_shop(data)

        self.assertIsInstance(shop, Shop)

    def test_get_or_create_shop_new_name(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop2', 'store_location': 'New Loc2'}
        shop = cmd._get_or_create_shop(data)

        self.assertEqual(shop.name, 'New Shop2')

    def test_get_or_create_shop_new_address(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop3', 'store_location': 'New Loc3'}
        shop = cmd._get_or_create_shop(data)

        self.assertEqual(shop.address, 'New Loc3')

    def test_get_or_create_shop_new_stats(self):
        cmd = self._get_command_instance()
        data = {'store_name': 'New Shop4', 'store_location': 'New Loc4'}
        cmd._get_or_create_shop(data)

        self.assertEqual(cmd.stats['shops_created'], 1)

    def test_get_or_create_shop_existing_instance(self):
        cmd = self._get_command_instance()
        existing_shop = Shop.objects.create(name="Existing Shop", address="Existing Loc")
        data = {'store_name': 'Existing Shop', 'store_location': 'Existing Loc'}
        shop = cmd._get_or_create_shop(data)

        self.assertEqual(shop, existing_shop)

    def test_get_or_create_shop_existing_stats(self):
        cmd = self._get_command_instance()
        Shop.objects.create(name="Existing Shop2", address="Existing Loc2")
        data = {'store_name': 'Existing Shop2', 'store_location': 'Existing Loc2'}
        cmd._get_or_create_shop(data)

        self.assertEqual(cmd.stats['shops_skipped'], 1)

    def test_get_or_create_product_new_instance(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product', 'store_product_id': 'NP1'}
        product = cmd._get_or_create_product(data)

        self.assertIsInstance(product, Product)

    def test_get_or_create_product_new_name(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product2', 'store_product_id': 'NP2'}
        product = cmd._get_or_create_product(data)

        self.assertEqual(product.name, 'New Product2')

    def test_get_or_create_product_new_store_product_id(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product3', 'store_product_id': 'NP3'}
        product = cmd._get_or_create_product(data)

        self.assertEqual(product.store_product_id, 'NP3')

    def test_get_or_create_product_new_stats(self):
        cmd = self._get_command_instance()
        data = {'product_name': 'New Product4', 'store_product_id': 'NP4'}
        cmd._get_or_create_product(data)

        self.assertEqual(cmd.stats['products_created'], 1)

    def test_get_or_create_product_existing_instance(self):
        cmd = self._get_command_instance()
        existing_product = Product.objects.create(name="Existing Product", store_product_id="EP1")
        data = {'product_name': 'Existing Product', 'store_product_id': 'EP1'}
        product = cmd._get_or_create_product(data)

        self.assertEqual(product, existing_product)

    def test_get_or_create_product_existing_stats(self):
        cmd = self._get_command_instance()
        Product.objects.create(name="Existing Product2", store_product_id="EP2")
        data = {'product_name': 'Existing Product2', 'store_product_id': 'EP2'}
        cmd._get_or_create_product(data)

        self.assertEqual(cmd.stats['products_skipped'], 1) 

# TODO: Add tests for price snapshot
