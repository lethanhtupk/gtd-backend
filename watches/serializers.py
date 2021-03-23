from rest_framework import serializers
from watches.models import (
    Watch
)
from products.models import (
    Brand, Category, Image, Product,
    Seller,
)
from django.contrib.auth.models import User
# third party library
import requests
from gtd_backend.utils import get_product_data, shorten_product_data, shorten_seller_data


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

            # TODO: create brand instance
            brand_data = product_data.get('brand')
            brand = None
            if brand_data:
                brand, brand_created = Brand.objects.update_or_create(
                    **brand_data)

            # TODO: create category instance
            category_data = product_data.get('categories')
            category = None
            if category_data:
                category, category_created = Category.objects.update_or_create(
                    **category_data)

            # FIXME: handle when seller is null
            seller_data = product_data.get('current_seller')
            seller = None
            if seller_data:
                brief_seller_data = shorten_seller_data(seller_data)
                seller, seller_created = Seller.objects.update_or_create(
                    **brief_seller_data
                )
            product, product_created = Product.objects.update_or_create(
                seller=seller,
                brand=brand,
                category=category,
                **brief_product_data,
            )

            # TODO: create image instance
            images_data = product_data.get('images')
            for image_data in images_data:
                Image.objects.update_or_create(
                    product=product,
                    **image_data
                )

                # FIXME: sometimes, tiki api automatically get rid of alphabet character to calling correct product
                # like product_id=2099555a will get the data of product with id=2099555
                # TODO: reassign product value for watch instance
            data['product'] = product_data['id']

            return super().to_internal_value(data)

        except Exception as e:
            raise e
