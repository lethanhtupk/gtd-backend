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
    re_path(
        'products/(?P<pk>[0-9]+)/update$',
        views.ProductUpdate.as_view(),
        name=views.ProductUpdate.name
    ),
    re_path(
        'products/(?P<pk>[0-9]+)/destroy$',
        views.ProductDestroy.as_view(),
        name=views.ProductDestroy.name
    ),
    path(
        'check-price/',
        views.CheckPrice.as_view(),
        name=views.CheckPrice.name
    ),
    path(
        'sellers/',
        views.SellerList.as_view(),
        name=views.SellerList.name
    ),
    re_path(
        'sellers/(?P<pk>[0-9]+)$',
        views.SellerDetail.as_view(),
        name=views.SellerDetail.name
    ),
    path(
        'products/search',
        views.SearchProduct.as_view(),
        name=views.SearchProduct.name
    ),
]
