from django.urls import path, re_path
from products import views

urlpatterns = [
  path(
    'products/', 
    views.ProductList.as_view(), 
    name=views.ProductList.name
  ),
  re_path(
    'products/(?P<pk>[0-9]+)$',
    views.ProductDetail.as_view(),
    name=views.ProductDetail.name
  ),
]