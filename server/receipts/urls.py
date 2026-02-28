from django.urls import path
from .views import ReceiptScanView, ReceiptScanProcessView

urlpatterns = [
    path('', ReceiptScanView.as_view(), name='receipts-list'),
    path('<int:scan_id>/', ReceiptScanView.as_view(), name='receipt-detail'),
    path('scan/', ReceiptScanProcessView.as_view(), name='receipt-scan'),
]