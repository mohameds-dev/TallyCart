from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'tags__name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer