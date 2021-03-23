
from rest_framework import (
    generics,
    serializers,
)
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from users.serializers import (UserProfileSerializer, RegisterSerializer)
from django.contrib.sites.shortcuts import get_current_site
# import permission classes
from gtd_backend.custompermission import (
    IsAdmin,
    IsAdminOrProfileOwner,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.urls import reverse
from gtd_backend.utils import send_email


# Create your views here.


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    name = 'register'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = CustomUser.objects.get(email=serializer.data.get('email'))

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')

        absurl = 'http://' + current_site + \
            relativeLink + '?token=' + str(token)

        data = {
            'name': user.fullname,
            'to_email': user.email,
            'verify_link': absurl,
        }

        send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VerifyEmail(generics.GenericAPIView):

    name = 'verify-email'

    def get():
        pass


class ProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-list'
    permission_classes = (IsAuthenticated, IsAdmin)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-detail'
    permission_classes = (IsAuthenticated, IsAdminOrProfileOwner)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if self.request.user.profile.role == 3:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
        else:
            if request.data.get('role'):
                raise serializers.ValidationError(
                    {'detail': 'You do not have permission to perform this action'})
            else:
                serializer = self.get_serializer(
                    instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_destroy(self, instance):
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().perform_destroy(instance)
