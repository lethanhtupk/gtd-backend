
from rest_framework import (
    generics,
    serializers
)
from users.models import UserProfile
from users.serializers import UserProfileSerializer

# import permission classes
from gtd_backend.custompermission import (
    IsAdmin,
    IsAdminOrProfileOwner,
)
from rest_framework.permissions import IsAuthenticated


# Create your views here.

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

    def perform_update(self, serializer):
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user.profile.role != 3:
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to perform this action'})
        return super().perform_destroy(instance)
