from django.urls import path, re_path
from users import views

urlpatterns = [
    path(
        'register/',
        views.RegisterView.as_view(),
        name=views.RegisterView.name
    ),
    path(
        'verify-email/',
        views.VerifyEmail.as_view(),
        name=views.VerifyEmail.name
    ),
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
]
