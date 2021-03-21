
from rest_framework import (
    generics,
    serializers,
)
from rest_framework.response import Response
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
