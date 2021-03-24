from rest_framework.permissions import IsAuthenticated
from gtd_backend.custompermission import IsAdmin
from rest_framework import generics
from products.models import (
    Product,
    Seller,
)
from products.serializers import (
    ProductCreateUpdateSerializer, ProductSerializer, SellerSerializer
)
from rest_framework.response import Response
from rest_framework import serializers
import requests
from gtd_backend.utils import get_product_data, shorten_product_data
# Create your views here.


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin,)
    name = 'product-list'

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.data.get('product_id')

        product_data = get_product_data(product_id)

        brief_product_data = shorten_product_data(product_data)

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
            **brief_product_data,
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
                product_data = get_product_data(product_id)
                brief_product_data = shorten_product_data(product_data)
                return Response(brief_product_data)
            else:
                return super().get(request, *args, **kwargs)


class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    name = 'product-update'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        product_id = request.data.get('product_id')
        product_data = get_product_data(product_id)

        brief_product_data = shorten_product_data(product_data)
        serializer = ProductSerializer(
            instance=instance, data=brief_product_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ProductDestroy(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    name = 'product-destroy'


class SellerList(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    name = 'seller-list'

    def create(self, request, *args, **kwargs):
        if (self.request.user.profile.role != 3):
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
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
