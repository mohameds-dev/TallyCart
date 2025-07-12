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
        product, created = Product.objects.get_or_create(name=validated_data['product_name'])
        if created:
            tags = self._create_tags(validated_data)
            product.tags.set(tags)
            product.save()

        return product

    def _create_tags(self, validated_data):
        return [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in validated_data.pop('tags').split(' ')]


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