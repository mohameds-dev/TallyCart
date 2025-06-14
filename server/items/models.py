from django.db import models

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
