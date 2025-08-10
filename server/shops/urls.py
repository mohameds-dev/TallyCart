from django.urls import path
from .views import ShopViewSet

urlpatterns = [
    path('', ShopViewSet.as_view({'get': 'list'}), name='shops'),
    path('<int:pk>/', ShopViewSet.as_view({'get': 'retrieve'}), name='shop'),
]
