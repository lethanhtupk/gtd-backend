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
import json 

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
        raise serializers.ValidationError({'product': 'required field'})
      if not expected_price:
        raise serializers.ValidationError({'expected_price': 'required field'})

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

      if int(data.get('expected_price')) > int(product_data.get('price')):
        raise serializers.ValidationError({'expected_price': 'expected_price cannot smaller than current price'})
      
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
      
      # FIXME: sometimes, tiki api automatically get rid of alphabet character to calling correct product 
      # like product_id=2099555a will get the data of product with id=2099555
      # TODO: reassign product value for watch instance
      data['product'] = product_data['id']

      return super().to_internal_value(data)

    except Exception as e:
      raise e

class UserSerializer(serializers.ModelSerializer):
  watches = WatchSerializer(
    many=True,
    read_only=True,
  )

  class Meta:
    model = User
    fields = '__all__'

