from rest_framework import serializers
from .models import Product, Tag, PriceSnapshot
from shops.models import Shop
from .utils import format_date, convert_price_to_float, validate_unit

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
    currency = serializers.CharField(required=False, allow_blank=True)
    source = serializers.CharField(required=False, allow_blank=True)


    def create(self, validated_data):
        product, _ = Product.objects.get_or_create(name=validated_data['product_name'])
        tags = self._create_tags(validated_data)
        product.tags.set(tags)
        product.save()
        
        shop, _ = Shop.objects.get_or_create(name=validated_data['store_name'], address=validated_data['store_location'])
        
        PriceSnapshot.objects.get_or_create(
            product=product,
            shop=shop,
            date=format_date(validated_data['date']),
            unit=validated_data['unit'],
            unit_price=convert_price_to_float(validated_data['unit_price']),
            store_product_id=validated_data['store_product_id'],
            currency=validated_data.get('currency', 'USD'),
            source=validated_data.get('source', 'manual input')
        )

        return product
    
    def validate(self, attrs):
        try:    
            validate_unit(attrs['unit'])
        except ValueError as e:
            raise serializers.ValidationError(e)
        return attrs

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