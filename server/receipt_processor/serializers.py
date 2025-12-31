from .models import ReceiptScan
from rest_framework import serializers

class ReceiptScanSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.pk

        return data

    class Meta:
        model = ReceiptScan
        fields = '__all__'
