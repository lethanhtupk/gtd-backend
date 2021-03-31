from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import CustomUser, Request, UserProfile
from products.serializers import SellerSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = ('is_seller', 'fullname')


class UserProfileSerializer(serializers.ModelSerializer):

    email = SerializerMethodField()
    user = UserSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'fullname',
                  'photo_url', 'role', 'user', 'seller')

    def update(self, instance, validated_data):
        fullname = validated_data.get('fullname')
        role = validated_data.get('role')
        user = instance.user
        if role:
            if role == 2:
                user.is_seller = True
            if role == 1:
                user.is_seller = False
            elif role == 3:
                raise serializers.ValidationError(
                    {'detail': 'Cannot set a user to be admin'})

        if fullname:
            user.fullname = fullname

        user.save()

        return super().update(instance, validated_data)

    def get_email(self, obj):
        return CustomUser.objects.get(profile=obj).email


class RequestCreateSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.user.email')

    class Meta:
        model = Request
        fields = ('seller', 'status', 'created_at', 'updated_at', 'owner')


class RequestUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user.email')

    class Meta:
        model = Request
        fields = ('status', 'reject_reason', 'owner',
                  'created_at', 'updated_at')

    def validate(self, attrs):
        status = attrs.get('status')
        reject_reason = attrs.get('reject_reason')
        if status == 2 and reject_reason:
            raise serializers.ValidationError(
                {'detail': 'Do not need reject reason for the request have been approve'})
        if status == 3 and not reject_reason:
            raise serializers.ValidationError(
                {'detail': 'You need to provide reason for your rejection'})
        return super().validate(attrs)
