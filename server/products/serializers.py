from rest_framework import serializers
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.utils import timezone
from .models import Product, Tag, PriceSnapshot
from shops.models import Shop


class CSVRowSerializer(serializers.Serializer):
    store_product_id = serializers.CharField(required=False, allow_blank=True)
    date = serializers.CharField(required=False, allow_blank=True)
    product_name = serializers.CharField(required=True, allow_blank=False)
    tags = serializers.CharField(required=False, allow_blank=True)
    unit = serializers.CharField(required=False, allow_blank=True)
    units_per_pack = serializers.CharField(required=False, allow_blank=True)
    packs_bought = serializers.CharField(required=False, allow_blank=True)
    sale_price = serializers.CharField(required=False, allow_blank=True)
    unit_price = serializers.CharField(required=True, allow_blank=False)
    store_name = serializers.CharField(required=False, allow_blank=True)
    store_location = serializers.CharField(required=False, allow_blank=True)

    def validate_unit_price(self, value):
        if not value:
            raise serializers.ValidationError("Unit price is required")
        
        cleaned_value = value.replace('$', '').replace(',', '').strip()
        
        try:
            price = Decimal(cleaned_value)
            if price < 0:
                raise serializers.ValidationError("Unit price must be non-negative")
            return price
        except (ValueError, InvalidOperation):
            raise serializers.ValidationError(f"Invalid unit price format: {value}")

    def validate_unit(self, value):
        if value and value.strip().upper() == 'TBD':
            raise serializers.ValidationError("Unit cannot be 'TBD'")
        return value

    def validate_date(self, value):
        if not value:
            return timezone.now().date()
        
        try:
            return datetime.strptime(value.strip(), '%m/%d/%Y').date()
        except ValueError:
            raise serializers.ValidationError(
                f"Date format not recognized: {value}. Expected m/d/Y (e.g., 2/20/2025)"
            )

    def validate(self, data):
        if not data.get('product_name') and not data.get('unit_price'):
            raise serializers.ValidationError("Both product_name and unit_price are required")
        
        return data

    def to_internal_value(self, data):
        mapped_data = {
            'store_product_id': data.get('store_product_id', ''),
            'date': data.get('date', ''),
            'product_name': data.get('product_name', ''),
            'tags': data.get('tags', ''),
            'unit': data.get('unit', ''),
            'units_per_pack': data.get('units_per_pack', ''),
            'packs_bought': data.get('packs_bought', ''),
            'sale_price': data.get('sale_price', ''),
            'unit_price': data.get('unit_price', ''),
            'store_name': data.get('store_name', ''),
            'store_location': data.get('store_location', ''),
        }
        
        return super().to_internal_value(mapped_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'store_product_id', 'tags']
        read_only_fields = ['id']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'address']
        read_only_fields = ['id']


class PriceSnapshotSerializer(serializers.ModelSerializer):    
    class Meta:
        model = PriceSnapshot
        fields = ['id', 'product', 'shop', 'date', 'unit', 'unit_price', 'currency', 'source']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id'] 