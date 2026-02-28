from django.contrib import admin
from .models import Product, Tag, PriceSnapshot

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Product, ProductAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Tag, TagAdmin)

class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'unit_price', 'currency', 'shop')
    list_filter = ('product', 'date', 'currency', 'shop')
    search_fields = ('product__name', 'shop__name')
    list_per_page = 10

admin.site.register(PriceSnapshot, PriceSnapshotAdmin)
