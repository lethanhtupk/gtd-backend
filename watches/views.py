from users import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics

# permission classes
from rest_framework.permissions import (
    IsAuthenticated
)
from gtd_backend.custompermission import (
    IsAdmin, IsAdminOrOwner
)

# serializer classes and model classes
from watches.serializers import (
    WatchSerializer,
)
from watches.models import (
    Watch,
)
from users.views import (
    ProfileList,
)
from products.views import (
    ProductList,
    SellerList,
)
# Create your views here.


class WatchList(generics.ListCreateAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    permission_classes = (IsAuthenticated,)
    name = 'watch-list'

    # TODO: only owner and admin can get the list of watches
    def list(self, request, *args, **kwargs):
        if (request.user.profile == 3):
            queryset = self.get_queryset()
        else:
            queryset = Watch.objects.filter(owner=request.user)
        serializer = WatchSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print('RUNNING create() method on View')
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


class WatchDetail(generics.RetrieveUpdateAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    name = 'watch-detail'
    # TODO: only admin and owner able to view, update detail of watch
    permission_classes = (
        IsAuthenticated,
        IsAdminOrOwner
    )

    # TODO: owner only can update the status and expected price of a watch
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if request.data.get('product'):
            raise serializers.ValidationError(
                {'detail': 'You can only update status and expected_price field'})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class WatchDestroy(generics.DestroyAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    name = 'watch-destroy'
    # TODO: only allow admin to delete watch instance
    permission_classes = (IsAuthenticated, IsAdmin)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'products': reverse(ProductList.name, request=request),
            'watches': reverse(WatchList.name, request=request),
            'sellers': reverse(SellerList.name, request=request),
            'profiles': reverse(ProfileList.name, request=request)
        })
