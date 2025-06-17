from django.db import models
from shops.models import Shop
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField(Tag, through='ItemTag', related_name='items')

    def __str__(self):
        return self.name[:50]

class ItemTag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('item', 'tag')

    def __str__(self):
        return f"{self.item} - TAGGED: {self.tag}"


class PriceSnapshot(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    unit = models.CharField(max_length=255, default="unit")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    source = models.CharField(max_length=255, default="manual input")
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('item', 'date', 'shop', 'unit')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['item', 'date']),
        ]

    def __str__(self):
        return f"{self.item} - FOR {self.unit_price:.2f} {self.currency} / {self.unit} - ON {self.date} {f'FROM {self.shop}' if self.shop else ''}"
