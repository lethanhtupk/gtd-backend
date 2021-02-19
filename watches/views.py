from watches.serializers import (
  ProductSerializer,
  WatchSerializer,  
)
from watches.models import (
  Watch,
  Product,
)
from rest_framework import generics 
# Create your views here.

class ProductList(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  # def perform_create(self, serializer):
  #   # calling external api in here

class WatchList(generics.ListCreateAPIView):
  queryset = Watch.objects.all()
  serializer_class = WatchSerializer
