from django.db import models
from core.models import User
from products.models import PriceSnapshot

class Order(models.Model):
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ORDERED BY: {self.ordered_by.username} # DATE: {self.date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price_snapshot = models.ForeignKey(PriceSnapshot, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price_snapshot.unit_price

    def __str__(self):
        return f"{self.price_snapshot.product} # QTY: {self.quantity} @ {self.price_snapshot.unit_price} / {self.price_snapshot.unit}"
