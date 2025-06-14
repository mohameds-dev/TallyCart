from django.db import models
from core.models import User
from items.models import Item

class Order(models.Model):
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    date = models.DateTimeField(auto_now_add=True)
    # shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"ORDERED BY: {self.ordered_by.username} - DATE: {self.date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.FloatField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20) 

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.item} - {self.quantity} @ {self.unit_price} / {self.unit}"
