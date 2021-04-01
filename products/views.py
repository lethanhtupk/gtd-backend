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
from gtd_backend.utils import get_product_data, search_product, shorten_product_data, update_or_create_brand, update_or_create_category, update_or_create_images, update_or_create_product, update_or_create_seller
from rest_framework import status
from djoser.conf import settings
from gtd_backend.utils import EmailThread
# Create your views here.


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin,)
    name = 'product-list'
    filter_fields = ('category', 'brand', 'seller')
    search_fields = ('name',)
    ordering_fields = ('-updated_at',)
    ordering = ('-updated_at',)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer

    def create(self, request, *args, **kwargs):
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
            return super().get(request, *args, **kwargs)
        # current user is normal user
        else:
            if not product:
                product_data = get_product_data(product_id)
                brief_product_data = shorten_product_data(product_data)
                return Response(brief_product_data)
            else:
                return super().get(request, *args, **kwargs)


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
                if product_price <= watch.expected_price and watch.status == 1:
                    email_lst.append(watch.owner.email)
                    watch.status = 3
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
        if (self.request.user.profile.role != 3):
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().create(request, *args, **kwargs)


class SellerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAuthenticated)
    name = 'seller-detail'


class FlashSaleProduct(generics.GenericAPIView):

    def get(self, request):
        pass


class SearchProduct(generics.GenericAPIView):
    name = 'product-search'

    def get(self, request):
        params = request.query_params
        data = search_product(params.get('q'), params.get('limit'))
        return Response(data=data, status=status.HTTP_200_OK)
