from django.test import TestCase
from items.models import Item, Tag, ItemTag
from django.db import IntegrityError


class ItemModelTests(TestCase):
    def test_canary(self):
        self.assertTrue(True)
    
    def test_item_str_representation(self):
        item = Item.objects.create(name="Test Item")
        self.assertEqual(str(item), "Test Item")

    def test_long_item_name_truncation(self):
        long_name = "This is a very long item name that should be truncated..."
        item = Item.objects.create(name=long_name)
        self.assertEqual(str(item), f"{long_name[:50]}")


class ItemTagModelTests(TestCase):
    def test_tag_str_representation(self):
        tag = Tag.objects.create(name="Test Tag")
        self.assertEqual(str(tag), "Test Tag")

    def test_item_tag_str_representation(self):
        item = Item.objects.create(name="Test Item")
        tag = Tag.objects.create(name="Test Tag")
        item_tag = ItemTag.objects.create(item=item, tag=tag)
        self.assertEqual(str(item_tag), f"{item} - TAGGED: {tag}")


    def test_item_tag_unique_together_constraint(self):
        item = Item.objects.create(name="Test Item")
        tag = Tag.objects.create(name="Test Tag")
        ItemTag.objects.create(item=item, tag=tag)
        with self.assertRaises(IntegrityError):
            ItemTag.objects.create(item=item, tag=tag)

    def test_count_multiple_tags_for_item(self):
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
