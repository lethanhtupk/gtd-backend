from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics

# permission classes
from rest_framework.permissions import (
  IsAuthenticated
)
from gtd_backend.custompermission import (
  IsAdmin
)

# serializer classes and model classes
from watches.serializers import (
  ProductSerializer, SellerSerializer,
  WatchSerializer,  
)
from watches.models import (
  Seller, Watch,
  Product,
)

from users.views import (
  ProfileList,
)
# Create your views here.

class ProductList(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  name = 'product-list'

class SellerList(generics.ListCreateAPIView):
  queryset = Seller.objects.all()
  serializer_class = SellerSerializer
  name = 'seller-list'

class ProductDetail(generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  name = 'product-detail'

class WatchList(generics.ListCreateAPIView):
  queryset = Watch.objects.all()
  serializer_class = WatchSerializer
  permission_classes = (IsAuthenticated,)
  name = 'watch-list'
  # TODO: only owner and admin can get the list of watches

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class WatchDetail(generics.RetrieveUpdateAPIView):
  queryset = Watch.objects.all()
  serializer_class = WatchSerializer
  name = 'watch-detail'
  # permission_classes = (
  #   permissions.IsAuthenticated,
  #   custompermission.IsCurrentUserOwnerOrReadOnly,
  # )
  # TODO: only admin and owner able to view detail of watch

class WatchDestroy(generics.DestroyAPIView):
  queryset = Watch.objects.all()
  serializer_class = WatchSerializer
  name = 'watch-destroy'
  # TODO: only allow admin to delete watch instance
  permissions = (IsAdmin)

class ApiRoot(generics.GenericAPIView):
  name = 'api-root'
  def get(self, request, *args, **kwargs):
    return Response({
      'products': reverse(ProductList.name, request=request),
      'watches': reverse(WatchList.name, request=request),
      'sellers': reverse(SellerList.name, request=request),
      'profiles': reverse(ProfileList.name, request=request)
    })