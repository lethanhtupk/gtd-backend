from rest_framework import serializers
from products.models import (
    Product,
    Seller
)
from watches.serializers import (
    WatchSerializer,
)


class ProductCreateSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):

    watches = WatchSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    products = ProductDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Seller
        fields = '__all__'
