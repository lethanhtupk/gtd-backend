from rest_framework import serializers
from watches.models import (
    Watch
)

from django.contrib.auth.models import User
# third party library
import requests
from gtd_backend.utils import get_product_data, product_data_for_create, shorten_seller_data, update_or_create_brand, update_or_create_category, update_or_create_images, update_or_create_product, update_or_create_seller


class WatchSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Watch
        fields = '__all__'

    def validate(self, attrs):
        status = attrs.get('status')
        if status == 3:
            raise serializers.ValidationError(
                {'status': 'Cannot manually set status of watch to FINISH'})
        return super().validate(attrs)

    def to_internal_value(self, data):
        try:
            product_id = data.get('product')
            expected_price = data.get('expected_price')
            if not product_id:
                raise serializers.ValidationError(
                    {'product': 'required field'})
            if not expected_price:
                raise serializers.ValidationError(
                    {'expected_price': 'required field'})

            product_data = get_product_data(product_id)

            if int(data.get('expected_price')) > int(product_data.get('price')):
                raise serializers.ValidationError(
                    {'expected_price': 'expected_price cannot bigger than current price'})

            brand = update_or_create_brand(product_data)
            category = update_or_create_category(product_data)
            seller = update_or_create_seller(product_data)

            product = update_or_create_product(
                product_data, brand, category, seller)

            update_or_create_images(product_data, product)

            data['product'] = product_data['id']

            return super().to_internal_value(data)

        except Exception as e:
            raise e


class WatchUpdateSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.SerializerMethodField()

    class Meta:
        model = Watch
        fields = ('id', 'owner', 'expected_price',
                  'status', 'created_at', 'updated_at', 'product')

    def get_product(self, obj):
        return obj.product.id

    def validate(self, attrs):
        status = attrs.get('status')
        if status == 3:
            raise serializers.ValidationError(
                {'status': 'Cannot manually change the status of watch to FINISH'})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        expected_price = validated_data.get(
            'expected_price', instance.expected_price)
        if expected_price > instance.product.price:
            raise serializers.ValidationError(
                {'expected_price': 'expected_price cannot be bigger than current price'})
        return super().update(instance, validated_data)
