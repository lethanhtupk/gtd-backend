
from rest_framework import (
    generics,
    serializers,
)
from rest_framework.response import Response
from users.models import CustomUser, UserProfile
from users.serializers import UserProfileSerializer

# import permission classes
from gtd_backend.custompermission import (
    IsAdmin,
    IsAdminOrProfileOwner,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# Create your views here.

class ProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-list'
    permission_classes = (IsAuthenticated, IsAdmin)


class CurrentUserProfile(generics.GenericAPIView):
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
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().perform_destroy(instance)
