from django.urls import path, re_path
from watches import views

urlpatterns = [
    path(
        'watches/',
        views.WatchList.as_view(),
        name=views.WatchList.name
    ),
    re_path(
        'watches/(?P<pk>[0-9]+)/delete$',
        views.WatchDestroy.as_view(),
        name=views.WatchDestroy.name
    ),
    re_path(
        'watches/(?P<pk>[0-9]+)/update$',
        views.WatchUpdate.as_view(),
        name=views.WatchUpdate.name
    ),
    re_path(
        'watches/(?P<pk>[0-9]+)$',
        views.WatchDetail.as_view(),
        name=views.WatchDetail.name
    ),
]
