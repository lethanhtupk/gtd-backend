from rest_framework import serializers
import requests

def get_product_data(product_id):
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
  return response.json()


def shorten_product_data(product_data):

  brief_product_data = {
    'id': product_data['id'],
    'name': product_data['name'], 
    'thumbnail_url': product_data['thumbnail_url'],
    'short_description': product_data['thumbnail_url'],
    'price': product_data['price'],
    'list_price': product_data['list_price'],
    'discount': product_data['discount'],
    'discount_rate': product_data['discount_rate'],
    'rating_average': product_data['rating_average'],
    'product_group_name': product_data['productset_group_name'],
    'description':product_data['description'],
  }

  return brief_product_data
    
