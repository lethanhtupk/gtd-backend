from rest_framework import serializers
from watches.models import (
    Watch
)
from products.models import (
    Product,
    Seller,
)
from django.contrib.auth.models import User
# third party library
import requests
from gtd_backend.utils import get_product_data, shorten_product_data


class WatchSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Watch
        fields = '__all__'

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
            brief_product_data = shorten_product_data(product_data)

            if int(data.get('expected_price')) > int(product_data.get('price')):
                raise serializers.ValidationError(
                    {'expected_price': 'expected_price cannot smaller than current price'})

            # FIXME: handle when seller is null
            seller = product_data.get('current_seller')
            obj = None
            if seller:
                obj, created = Seller.objects.get_or_create(
                    id=seller['id'],
                    name=seller['name'],
                    link=seller['link'],
                    logo=seller['logo'],
                )
            Product.objects.update_or_create(
                seller=obj,
                **brief_product_data,
            )

            # FIXME: sometimes, tiki api automatically get rid of alphabet character to calling correct product
            # like product_id=2099555a will get the data of product with id=2099555
            # TODO: reassign product value for watch instance
            data['product'] = product_data['id']

            return super().to_internal_value(data)

        except Exception as e:
            raise e
