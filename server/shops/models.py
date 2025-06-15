from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    url = models.URLField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)

    class Meta:
        db_table = 'shops'

    def __str__(self):
        return f"{self.name}{(f' at {self.address}') if self.address else ''}"
