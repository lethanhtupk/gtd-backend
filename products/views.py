from rest_framework.permissions import IsAuthenticated
from gtd_backend.custompermission import IsAdmin
from rest_framework import generics
from products.models import (
  Product,
  Seller,
)
from products.serializers import (
  ProductCreateSerializer, ProductSerializer, SellerSerializer
)
from rest_framework.response import Response
from rest_framework import serializers
import requests
# Create your views here.


class ProductList(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  permission_classes = (IsAuthenticated, IsAdmin,)
  name = 'product-list'

  def get_serializer_class(self, *args, **kwargs):
    if self.request.method == 'POST':
      return ProductCreateSerializer
    return ProductSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product_id = serializer.data.get('product_id')

    headers = {
        'authority': 'scrapeme.live',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
      }

    response = requests.get(f"https://tiki.vn/api/v2/products/{product_id}", headers=headers)
    if response.status_code != 200:
      raise serializers.ValidationError({'product': "cannot find any product with that ID"})

    product_data = response.json()

    seller = product_data.get('current_seller')
    obj = None
    if seller:
      obj, created = Seller.objects.get_or_create(
        id=seller['id'], 
        name=seller['name'], 
        link=seller['link'],
        logo=seller['logo'],
      )
      
    product, created = Product.objects.update_or_create(
      seller=obj,
      id=product_data['id'], 
      name=product_data['name'], 
      thumbnail_url=product_data['thumbnail_url'],
      short_description=product_data['thumbnail_url'],
      price=product_data['price'],
      list_price=product_data['list_price'],
      discount=product_data['discount'],
      discount_rate=product_data['discount_rate'],
      rating_average=product_data['rating_average'],
      product_group_name=product_data['productset_group_name'],
      description=product_data['description'],
    )

    product_serializer = ProductSerializer(instance=product)
    return Response(product_serializer.data)

class ProductDetail(generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  permission_classes = (IsAuthenticated,)
  name = 'product-detail'
  
  def get(self, request, *args, **kwargs):
    product_id = kwargs.get('pk')
    try:
      product = Product.objects.get(pk=product_id)
    except:
      product = None
    # current user is Admin
    if self.request.user.profile.role == 3:
      if not product:
        raise serializers.ValidationError({'detail': 'Not found'})
      return super().get(*args, **kwargs)
    # current user is normal user
    else:
      if not product:
        headers = {
          'authority': 'scrapeme.live',
          'dnt': '1',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'sec-fetch-site': 'none',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-user': '?1',
          'sec-fetch-dest': 'document',
          'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        response = requests.get(f"https://tiki.vn/api/v2/products/{product_id}", headers=headers)
        if response.status_code != 200:
          raise serializers.ValidationError({'product': "cannot find any product with that ID"})

        product_data = response.json()
        return Response(product_data)
      else:
        return super().get(request, *args, **kwargs)

class ProductDestroy(generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  permission_classes = (IsAuthenticated, IsAdmin)

class SellerList(generics.ListCreateAPIView):
  queryset = Seller.objects.all()
  serializer_class = SellerSerializer
  name = 'seller-list'

  def create(self, request, *args, **kwargs):
    if (self.request.user.profile.role != 3):
      raise serializers.ValidationError({'detail': 'You do not have permission to perform this action'})
    return super().create(request, *args, **kwargs)


class SellerDetail(generics.RetrieveAPIView):
  queryset = Seller.objects.all()
  serializer_class = SellerSerializer
  name = 'seller-detail'

class SellerUpdate(generics.UpdateAPIView):
  queryset = Seller.objects.all()
  serializer_class = SellerSerializer
  name = 'seller-update'

class SellerDestroy(generics.DestroyAPIView):
  queryset = Seller.objects.all()
  serializer_class = SellerSerializer
  name = 'seller-destroy'