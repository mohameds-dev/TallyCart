from django.test import TestCase
from items.models import Item, Tag, ItemTag, PriceSnapshot
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from shops.models import Shop
from datetime import date

class ItemModelTests(TestCase):
    def test_canary(self):
        self.assertTrue(True)

    def test_item_name_uniqueness(self):
        Item.objects.create(name="Test Item")
        with self.assertRaises(IntegrityError):
            Item.objects.create(name="Test Item")

    def test_item_name_exceeding_max_length_raises_validation_error_with_full_clean_and_save(self):
        item = Item(name="A" * 256)
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()
    
    def test_item_str_representation(self):
        item = Item.objects.create(name="Test Item")
        self.assertEqual(str(item), "Test Item")

    def test_long_item_name_truncation(self):
        long_name = "This is a very long item name that should be truncated..."
        item = Item.objects.create(name=long_name)
        self.assertEqual(str(item), f"{long_name[:50]}")


class ItemTagModelTests(TestCase):
    def test_tag_str_representation_correctness(self):
        tag = Tag.objects.create(name="Test Tag")
        self.assertEqual(str(tag), "Test Tag")

    def test_item_tag_str_representation_correctness(self):
        item = Item.objects.create(name="Test Item")
        tag = Tag.objects.create(name="Test Tag")
        item_tag = ItemTag.objects.create(item=item, tag=tag)
        self.assertEqual(str(item_tag), f"{item} - TAGGED: {tag}")


    def test_item_tag_unique_together_constraint_prevents_duplicate_tags_on_same_item(self):
        item = Item.objects.create(name="Test Item")
        tag = Tag.objects.create(name="Test Tag")
        ItemTag.objects.create(item=item, tag=tag)
        with self.assertRaises(IntegrityError):
            ItemTag.objects.create(item=item, tag=tag)

    def test_count_multiple_tags_for_item_correctness(self):
        item = Item.objects.create(name="Test Item")
        tag1 = Tag.objects.create(name="Test Tag 1")
        tag2 = Tag.objects.create(name="Test Tag 2")
        ItemTag.objects.create(item=item, tag=tag1)
        ItemTag.objects.create(item=item, tag=tag2)
        self.assertEqual(item.tags.count(), 2)

    def test_retrieving_items_by_tag(self):
        item1 = Item.objects.create(name="Item 1")
        item2 = Item.objects.create(name="Item 2")
        tag = Tag.objects.create(name="Test Tag")
        ItemTag.objects.create(item=item1, tag=tag)
        ItemTag.objects.create(item=item2, tag=tag)
        items = Item.objects.filter(tags=tag)
        
        self.assertEqual(list(items), [item1, item2])


class PriceSnapshotModelTests(TestCase):
    def test_price_snapshot_str_representation_correctness(self):
        item = Item.objects.create(name="Test Item")
        shop = Shop.objects.create(name="Test Shop")
        price_snapshot = PriceSnapshot.objects.create(item=item, shop=shop, unit_price=100)
        
        self.assertEqual(str(price_snapshot), f"{item} - FOR 100.00 USD / unit - ON {price_snapshot.date} FROM {shop}")

    def test_price_snapshot_unique_together_constraint_prevents_duplicate_price_snapshots_for_same_item_and_shop(self):
        item = Item.objects.create(name="Test Item")
        shop = Shop.objects.create(name="Test Shop")
        PriceSnapshot.objects.create(item=item, shop=shop, unit_price=100)

        with self.assertRaises(IntegrityError):
            PriceSnapshot.objects.create(item=item, shop=shop, unit_price=100)

    def test_price_snapshot_retrieves_records_ordered_by_most_recent(self):
        item1 = Item.objects.create(name="Test Item 1")
        item2 = Item.objects.create(name="Test Item 2")
        shop = Shop.objects.create(name="Test Shop")
        PriceSnapshot.objects.create(item=item1, shop=shop, unit_price=100, date=date(2021, 1, 1))
        PriceSnapshot.objects.create(item=item2, shop=shop, unit_price=200, date=date(2021, 1, 2))

        self.assertEqual(list(PriceSnapshot.objects.all()), [
            PriceSnapshot.objects.get(unit_price=200),
            PriceSnapshot.objects.get(unit_price=100),
        ])
