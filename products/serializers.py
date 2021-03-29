from django.utils import tree
from rest_framework import serializers
from products.models import (
    Brand, Image, Product,
    Seller, Category
)
from watches.serializers import (
    WatchSerializer,
)


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class Category(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class ProductCreateSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):

    watches = WatchSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    category = Category(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
