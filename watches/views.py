from rest_framework import generics, serializers

# permission classes
from rest_framework.permissions import (
    IsAuthenticated
)
from gtd_backend.custompermission import (
    IsAdmin, IsAdminOrOwner
)

# serializer classes and model classes
from watches.serializers import (
    WatchSerializer, WatchUpdateSerializer,
)
from watches.models import (
    Watch,
)
# Create your views here.


class WatchList(generics.ListCreateAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    permission_classes = (IsAuthenticated,)
    name = 'watch-list'
    filter_fields = ('status', 'owner')
    search_fields = ('product__name',)
    ordering_fields = ('-updated_at')
    ordering = ('-updated_at')

    def get_queryset(self):
        if self.request.user.profile.role == 3:
            return Watch.objects.all()
        elif self.request.user.profile.role == 2:
            if self.request.user.profile.seller:
                return Watch.objects.filter(product__seller=self.request.user.profile.seller)
            else:
                raise serializers.ValidationError(
                    {'detail': 'Your account haven\'t connected to any seller'})
        return Watch.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.data.get('product')
        watches = Watch.objects.filter(product=product, owner=request.user)
        if len(watches) > 0:
            raise serializers.ValidationError(
                {'product': 'Cannot create 2 watches with the same product ID'})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WatchDetail(generics.RetrieveAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    name = 'watch-detail'
    # TODO: only admin and owner able to view, update detail of watch
    permission_classes = (
        IsAuthenticated,
        IsAdminOrOwner
    )


class WatchUpdate(generics.UpdateAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchUpdateSerializer
    name = 'watch-update'
    permission_classes = (
        IsAuthenticated,
        IsAdminOrOwner
    )


class WatchDestroy(generics.DestroyAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    name = 'watch-destroy'
    # TODO: only allow admin to delete watch instance
    permission_classes = (IsAuthenticated, IsAdmin)
