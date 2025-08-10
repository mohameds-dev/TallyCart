from .models import ReceiptScan
from rest_framework import serializers

class ReceiptScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptScan
        fields = '__all__'