from products.models import Seller
from rest_framework import serializers
from django.core.mail import EmailMessage
import requests
from products.models import (
    Brand,
    Seller,
    Category,
    Image,
    Product
)

import threading


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

    response = requests.get(
        f"https://tiki.vn/api/v2/products/{product_id}", headers=headers)
    if response.status_code != 200:
        raise serializers.ValidationError(
            {'product': "cannot find any product with that ID"})
    return response.json()

# def get_flash_sale_data():
#     headers = {
#         'authority': 'scrapeme.live',
#         'dnt': '1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'sec-fetch-site': 'none',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-user': '?1',
#         'sec-fetch-dest': 'document',
#         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     }

#     response = requests.get(
#         f"https://tiki.vn/api/v2/products/{product_id}", headers=headers)
#     if response.status_code != 200:
#         raise serializers.ValidationError(
#             {'product': "cannot find any product with that ID"})
#     return response.json()


def search_product(search_pattern, limit, page):
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
    response = requests.get(
        f"https://tiki.vn/api/v2/products/?limit={limit}&q={search_pattern}&page={page}", headers=headers)
    if response.status_code != 200:
        raise serializers.ValidationError(
            {'detail': "Something went wrong"})
    return response.json()


def update_or_create_brand(product_data):
    brand_data = product_data.get('brand')
    brand = None
    if brand_data:
        brand, brand_created = Brand.objects.update_or_create(
            id=brand_data.get('id'), defaults=brand_data)

    return brand


def update_or_create_seller(product_data):
    seller_data = product_data.get('current_seller')
    seller = None
    if seller_data:
        brief_seller_data = shorten_seller_data(seller_data)
        seller, seller_created = Seller.objects.update_or_create(
            id=brief_seller_data.get('id'), defaults=brief_seller_data)

    return seller


def update_or_create_category(product_data):
    category_data = product_data.get('categories')
    category = None
    if category_data:
        category, category_created = Category.objects.update_or_create(
            id=category_data.get('id'), defaults=category_data)

    return category


def update_or_create_product(product_data, brand, category, seller):
    brief_product_data = product_data_for_create(product_data)
    product, product_created = Product.objects.update_or_create(
        id=product_data.get('id'), defaults={**brief_product_data, 'brand': brand, 'category': category, 'seller': seller})

    return product


def update_or_create_images(product_data, product):
    images = product_data['images']
    for image in images:
        Image.objects.update_or_create(
            product=product, base_url=image['base_url'], defaults=image)


def shorten_product_data(product_data):
    '''
    return product data without saving into DB
    '''

    brief_product_data = {
        'id': product_data['id'],
        'url_path': product_data['url_path'],
        'name': product_data['name'],
        'thumbnail_url': product_data['thumbnail_url'],
        'short_description': product_data['short_description'],
        'price': product_data['price'],
        'list_price': product_data['list_price'],
        'discount': product_data['discount'],
        'discount_rate': product_data['discount_rate'],
        'rating_average': product_data['rating_average'],
        'product_group_name': product_data['productset_group_name'],
        'brand': product_data.get('brand'),
        'seller': product_data.get('current_seller'),
        'category': product_data.get('categories'),
        'images': product_data.get('images'),
        'description': product_data['description'],
    }

    return brief_product_data


def product_data_for_create(product_data):
    ''''
    prepare data for saving into DB
    '''

    brief_product_data = {
        'id': product_data['id'],
        'url_path': product_data['url_path'],
        'name': product_data['name'],
        'thumbnail_url': product_data['thumbnail_url'],
        'short_description': product_data['short_description'],
        'price': product_data['price'],
        'list_price': product_data['list_price'],
        'discount': product_data['discount'],
        'discount_rate': product_data['discount_rate'],
        'rating_average': product_data['rating_average'],
        'product_group_name': product_data['productset_group_name'],
        'description': product_data['description'],
    }

    return brief_product_data


def shorten_seller_data(seller_data):
    '''
    prepare data for saving seller into DB
    '''
    return {
        'id': seller_data['id'],
        'sku': seller_data['sku'],
        'name': seller_data['name'],
        'slug': seller_data['slug'],
        'link': seller_data['link'],
        'is_best_store': seller_data['is_best_store'],
        'logo': seller_data['logo'],
    }


class EmailThread(threading.Thread):

    def __init__(self, email, to):
        self.to = to
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(self.to)
