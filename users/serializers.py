from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import CustomUser, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'CustomUserSerializer'
        model = CustomUser
        fields = ('is_seller', 'fullname')


class UserProfileSerializer(serializers.ModelSerializer):

    email = SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'fullname', 'photo_url', 'role', 'user')

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
