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
  path(
    'sellers/', 
    views.SellerList.as_view(), 
    name=views.SellerList.name
  ),
  re_path(
    'products/(?P<pk>[0-9]+)$',
    views.SellerDetail.as_view(),
    name=views.SellerDetail.name
  ),
  re_path(
    'products/(?P<pk>[0-9]+)$',
    views.SellerUpdate.as_view(),
    name=views.SellerUpdate.name
  ),
  re_path(
    'products/(?P<pk>[0-9]+)$',
    views.SellerDestroy.as_view(),
    name=views.SellerDestroy.name
  ),
]