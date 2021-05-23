from rest_framework.permissions import IsAuthenticated
from gtd_backend.custompermission import IsAdmin
from rest_framework import generics
from products.models import (
    Product,
    Seller,
)
from products.serializers import (
    ProductCreateSerializer, ProductNonAuthOrCustomerSerializer, ProductSerializer, SellerSerializer, ProductViewSerializer
)
from rest_framework.response import Response
from rest_framework import serializers
from gtd_backend.utils import get_product_data, search_product, shorten_product_data, update_or_create_brand, update_or_create_category, update_or_create_images, update_or_create_product, update_or_create_seller
from rest_framework import status
from djoser.conf import settings
from gtd_backend.utils import EmailThread
from django_filters import rest_framework as filters
# Create your views here.


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    name = 'product-list'
    filter_fields = ('category', 'brand', 'seller')
    search_fields = ('name',)
    ordering_fields = ('-updated_at', 'price',
                       'discount_rate', 'discount', 'watch_count', '-watch_count')
    ordering = ('-updated_at',)

    def get_queryset(self):
        if self.request.user.profile.role == 3:
            return Product.objects.all()
        elif self.request.user.profile.role == 2:
            if self.request.user.profile.seller:
                return Product.objects.filter(seller=self.request.user.profile.seller)
            else:
                raise serializers.ValidationError(
                    {'detail': 'You haven\'t connected to any seller yet'})
        else:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.data.get('product_id')

        product_data = get_product_data(product_id)

        brand = update_or_create_brand(product_data)
        seller = update_or_create_seller(product_data)
        category = update_or_create_category(product_data)

        product = update_or_create_product(
            product_data, brand, category, seller)

        update_or_create_images(product_data, product)

        product_serializer = ProductSerializer(instance=product)
        return Response(product_serializer.data)


class ProductViewList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductViewSerializer
    name = 'product-view-list'
    ordering_fields = ('-updated_at', 'price',
                       'discount_rate', 'discount', 'watch_count', '-watch_count')
    ordering = ('-updated_at',)


class ProductDetailDisplay(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductNonAuthOrCustomerSerializer
    name = 'product-detail-display'

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product_data = get_product_data(product_id)
        brief_product_data = shorten_product_data(product_data)
        return Response(brief_product_data, status=status.HTTP_200_OK)


class ProductDetailManage(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    name = 'product-detail-manage'

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        if self.request.user.profile.role == 2:
            if product.seller != self.request.user.profile.seller:
                raise serializers.ValidationError(
                    {'detail': 'You do not have permission to perform this action'})
        elif self.request.user.profile.role == 1:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})

        return super().retrieve(request, *args, **kwargs)


class ProductUpdate(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (IsAuthenticated,)
    name = 'product-update'

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_id)
            product_data = get_product_data(product_id)

            brand = update_or_create_brand(product_data)
            seller = update_or_create_seller(product_data)
            category = update_or_create_category(product_data)

            product = update_or_create_product(
                product_data, brand, category, seller)

            serializer = self.get_serializer(product)

            update_or_create_images(product_data, product)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            raise serializers.ValidationError({'detail': 'Not found'})


class ProductDestroy(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    name = 'product-destroy'


class CheckPrice(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    name = 'check-price'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        for product in products:

            product_data = get_product_data(product.id)

            brand = update_or_create_brand(product_data)
            category = update_or_create_category(product_data)
            seller = update_or_create_seller(product_data)

            product = update_or_create_product(
                product_data, brand, category, seller)

            update_or_create_images(product_data, product)

            product_price = product_data.get('price')

            email_lst = []
            for watch in product.watches.all():
                if product_price <= watch.expected_price and product_price <= watch.lowest_price and watch.status == 1:
                    email_lst.append(watch.owner.email)
                    watch.lowest_price = product_price
                    watch.save()
            currency = "{:,}".format(product_price)
            new_currency = currency.replace(',', '.')
            context = {'product': product, 'price': new_currency}
            email = settings.EMAIL.informing(self.request, context)
            EmailThread(email, email_lst).start()
        return Response({'detail': 'Successfully check the price and send email to users'}, status=status.HTTP_200_OK)


class SellerList(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    name = 'seller-list'

    def create(self, request, *args, **kwargs):
        if (self.request.user and self.request.user.profile.role != 3):
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
    permission_classes = (IsAuthenticated, IsAdmin)
    name = 'seller-update'


class SellerDestroy(generics.DestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    name = 'seller-destroy'


class SearchProduct(generics.GenericAPIView):
    name = 'product-search'

    def get(self, request):
        params = request.query_params
        limit = params.get('limit') if params.get('limit') else 48
        page = params.get('page') if params.get('page') else 1
        data = search_product(params.get('search'), limit, page)
        return Response(data=data, status=status.HTTP_200_OK)
