
from rest_framework import (
    generics,
    serializers,
)
from rest_framework.response import Response
from users.models import Request, UserProfile
from users.serializers import RequestCreateSerializer, RequestUpdateSerializer, UserProfileSerializer
# import permission classes
from gtd_backend.custompermission import (
    IsAdmin,
    IsAdminOrProfileOwner, IsAdminOrRequestOwner,
)
from rest_framework.permissions import IsAuthenticated
from products.models import Seller
from rest_framework import status
from djoser.conf import settings
from gtd_backend.utils import EmailThread


# Create your views here.

class ProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    name = 'profile-list'


class CurrentUserProfile(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    name = 'profile-me'

    def get(self, request):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer = self.get_serializer(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-detail'
    permission_classes = (IsAuthenticated, IsAdminOrProfileOwner)

    def update(self, request, *args, **kwargs):
        role = request.data.get('role')
        profile_id = kwargs.get('pk')
        if int(self.request.user.profile.id) == int(profile_id) and role:
            raise serializers.ValidationError(
                {'detail': 'You cannot change your own role'})
        if role != None and self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().perform_destroy(instance)


class RequestList(generics.ListCreateAPIView):
    serializer_class = RequestCreateSerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ('status', 'seller')
    ordering_fields = ('-updated_at', 'updated_at')
    ordering = ('-updated_at',)
    name = 'request-list'

    def get_queryset(self):
        if self.request.user.profile.role == 3:
            return Request.objects.all()
        elif self.request.user.profile.role == 2:
            return Request.objects.filter(owner=self.request.user.profile)
        raise serializers.ValidationError(
            {'detail': 'You do not have permission to perform this action'}) 

    def create(self, request, *args, **kwargs):
        if self.request.user.profile.role != 2:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        if self.request.user.profile.seller:
            raise serializers.ValidationError(
                {'detail': 'Your account already connected with a seller'})
        if len(Request.objects.filter(owner=self.request.user.profile)) > 0:
            raise serializers.ValidationError(
                {'detail': 'A user cannot request to connect more than 1 seller'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seller_id = serializer.data.get('seller')
        seller_instance = Seller.objects.get(id=seller_id)
        context = {'profile': self.request.user.profile,
                   'seller': seller_instance}
        email = settings.EMAIL.receive_request(self.request, context)
        EmailThread(email, [self.request.user.email]).start()
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user.profile)


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestUpdateSerializer
    permission_classes = (IsAuthenticated, IsAdminOrRequestOwner)
    name = 'request-detail'

    # TODO: send an email inform user that the request have been approve or reject
    def update(self, request, *args, **kwargs):
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})

        request_obj = self.get_object()

        serializer = self.get_serializer(
            instance=request_obj)
        incoming_data = self.get_serializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        owner = serializer.data.get('owner')
        seller = serializer.data.get('seller')
        context = {'status': incoming_data.data,
                   'owner': owner, 'seller': seller}
        email = settings.EMAIL.response_request(self.request, context)
        EmailThread(email, [owner.get('email')]).start()

        if int(incoming_data.data.get('status')) == 3:
            profile = request_obj.owner
            profile.seller = None
            profile.save()
            return super().destroy(request, *args, **kwargs)

        return super().update(request, *args, **kwargs)
