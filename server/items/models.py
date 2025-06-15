from django.db import models
from shops.models import Shop

class PriceSnapshot(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    unit = models.CharField(max_length=255, default="unit")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255, default="manual input")

    class Meta:
        db_table = 'item_price_snapshot'
        unique_together = ('item', 'date', 'unit')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['item', 'date']),
        ]

    def __str__(self):
        return f"{self.price} on {self.date}"

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'items_tag'

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField(Tag, through='ItemTag', related_name='items')

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.name[:50]

class ItemTag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'item_tag'
        unique_together = ('item', 'tag')

    def __str__(self):
        return f"{self.item} - TAGGED: {self.tag}"
