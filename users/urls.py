from django.urls import path, re_path
from users import views

urlpatterns = [
    path(
        'profiles/',
        views.ProfileList.as_view(),
        name=views.ProfileList.name
    ),
    re_path(
        'profiles/(?P<pk>[0-9]+)$',
        views.ProfileDetail.as_view(),
        name=views.ProfileDetail.name
    ),
    path(
        'profiles/me/',
        views.CurrentUserProfile.as_view(),
        name=views.CurrentUserProfile.name
    ),
    path(
        'requests/',
        views.RequestList.as_view(),
        name=views.RequestList.name
    ),
    re_path(
        'requests/(?P<pk>[0-9]+)$',
        views.RequestDetail.as_view(),
        name=views.RequestDetail.name
    ),

    # path(
    #   'watches/',
    #   views.WatchList.as_view(),
    #   name=views.WatchList.name
    # ),
    # re_path(
    #   'watches/(?P<pk>[0-9]+)/delete/$',
    #   views.WatchDestroy.as_view(),
    #   name=views.WatchDestroy.name
    # ),
    # re_path(
    #   'watches/(?P<pk>[0-9]+)$',
    #   views.WatchDetail.as_view(),
    #   name=views.WatchDetail.name
    # ),
    # path(
    #   'sellers/',
    #   views.SellerList.as_view(),
    #   name=views.SellerList.name
    # ),
    # path(
    #   '',
    #   views.ApiRoot.as_view(),
    #   name=views.ApiRoot.name
    # )
]
