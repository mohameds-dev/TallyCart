from django.db import models

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]

class ReceiptScan(models.Model):
    image = models.ImageField(upload_to='uploaded_receipt_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ocr_text = models.TextField(blank=True)
    receipt_data = models.JSONField(default=dict, blank=True)
    processing_steps = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"ReceiptScan {self.id}"
