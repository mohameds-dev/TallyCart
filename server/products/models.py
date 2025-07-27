from django.db import models
from shops.models import Shop
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField(Tag, through='ProductTag', related_name='products')

    def __str__(self):
        return self.name[:50]

class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'tag')

    def __str__(self):
        return f"{self.product} - TAGGED: {self.tag}"


class PriceSnapshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store_product_id = models.CharField(max_length=255, blank=True, null=True, help_text="Optional store-specific product ID")
    date = models.DateField(default=timezone.now)
    unit = models.CharField(max_length=255, default="unit")
    unit_price = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.CharField(max_length=3, default="USD")
    source = models.CharField(max_length=255, default="manual input")
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('product', 'date', 'unit', 'unit_price', 'currency', 'shop')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['product', 'date']),
        ]

    def __str__(self):
        return f"{self.product} - FOR {self.unit_price:.2f} {self.currency} / {self.unit} - ON {self.date} {f'FROM {self.shop}' if self.shop else ''}"
