from django.contrib import admin
from .models import ReceiptScan

class ReceiptScanAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('id', 'image')
    list_per_page = 10

admin.site.register(ReceiptScan, ReceiptScanAdmin)
