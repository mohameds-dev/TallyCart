from django.db import models
from orders.models import Order

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField(Tag, through='ItemTag', related_name='items')

    def __str__(self):
        return self.name

class ItemTag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('item', 'tag')

    def __str__(self):
        return f"{self.item.name[:50]} - TAGGED: {self.tag.name}"
