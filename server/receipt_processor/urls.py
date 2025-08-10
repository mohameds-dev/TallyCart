from django.urls import path
from .views import ReceiptsScanRetrievalView, ReceiptsScanProcessingView

urlpatterns = [
    path('', ReceiptsScanRetrievalView.as_view(), name='receipts-list'),
    path('<int:scan_id>/', ReceiptsScanRetrievalView.as_view(), name='receipt-detail'),
    path('scan/', ReceiptsScanProcessingView.as_view(), name='receipt-scan'),
]