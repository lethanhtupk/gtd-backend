from django.urls import path, re_path
from watches import views

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
    'watches/', 
    views.WatchList.as_view(), 
    name=views.WatchList.name
  ),
  re_path(
    'watches/(?P<pk>[0-9]+)/delete/$',
    views.WatchDestroy.as_view(),
    name=views.WatchDestroy.name
  ),
  re_path(
    'watches/(?P<pk>[0-9]+)$',
    views.WatchDetail.as_view(),
    name=views.WatchDetail.name
  ),
  path(
    'sellers/',
    views.SellerList.as_view(),
    name=views.SellerList.name
  ),
  path(
    '',
    views.ApiRoot.as_view(),
    name=views.ApiRoot.name
  )
]