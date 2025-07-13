from rest_framework import serializers
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.utils import timezone
from .models import Product, Tag, PriceSnapshot
from shops.models import Shop


class CSVRowSerializer(serializers.Serializer):
    store_product_id = serializers.CharField(required=False, allow_blank=True)
    date = serializers.CharField(required=True)
    product_name = serializers.CharField(required=True, allow_blank=False)
    tags = serializers.CharField(required=False, allow_blank=True)
    unit = serializers.CharField(required=True, allow_blank=False)
    units_per_pack = serializers.CharField(required=True, allow_blank=False)
    packs_bought = serializers.CharField(required=True, allow_blank=False)
    sale_price = serializers.CharField(required=True, allow_blank=False)
    unit_price = serializers.CharField(required=True, allow_blank=False)
    store_name = serializers.CharField(required=True, allow_blank=False)
    store_location = serializers.CharField(required=False, allow_blank=True)


    def create(self, validated_data):
        product, _ = Product.objects.get_or_create(name=validated_data['product_name'])
        tags = self._create_tags(validated_data)
        product.tags.set(tags)
        product.save()
        PriceSnapshot.objects.create(
            product=product,
            shop=Shop.objects.get_or_create(name=validated_data['store_name'], address=validated_data['store_location'])[0],
            date=self._format_date(validated_data['date']),
            unit=validated_data['unit'],
            unit_price=self._convert_price_to_float(validated_data['unit_price']),
        )

        return product
    
    def validate(self, attrs):
        self._validate_unit(attrs['unit'])
        return attrs

    def _create_tags(self, validated_data):
        return [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in validated_data.pop('tags').split(' ')]

    def _format_date(self, date_string):
        return datetime.strptime(date_string, '%m/%d/%Y')
    
    def _convert_price_to_float(self, price_string):
        return float(price_string.replace('$', ''))

    def _validate_unit(self, unit):
        if unit == 'some invalid unit':
            raise serializers.ValidationError(f"Invalid unit: {unit}")


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