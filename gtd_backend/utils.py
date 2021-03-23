from products.models import Seller
from rest_framework import serializers
from django.core.mail import EmailMessage
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

    response = requests.get(
        f"https://tiki.vn/api/v2/products/{product_id}", headers=headers)
    if response.status_code != 200:
        raise serializers.ValidationError(
            {'product': "cannot find any product with that ID"})
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
        'description': product_data['description'],
    }

    return brief_product_data


def shorten_seller_data(seller_data):
    return {
        'id': seller_data['id'],
        'sku': seller_data['sku'],
        'name': seller_data['name'],
        'slug': seller_data['slug'],
        'link': seller_data['link'],
        'is_best_store': seller_data['is_best_store'],
        'logo': seller_data['logo'],
    }


def send_email(data):
    subject = '[GetTheDeal] Xác nhận tài khoản'
    body = "Xin chào {fullname},\nCảm ơn đã đăng ký sử dụng dịch vụ của chúng tôi!\nChúng tôi cần thêm thông tin để hoàn thành quá trình đăng ký, bao gồm việc xác nhận lại địa chỉ email\nClick vào link bên dưới để xác nhận địa chỉ email của bạn:\n\n{verify_link}\nNếu bạn gặp vấn đề gì, hãy dán đường dẫn trên vào trình duyệt của bạn."

    email = EmailMessage(to=[data['to_email']],
                         subject=subject,  body=body.format(fullname=data['name'], verify_link=data['verify_link']))
    email.send()
