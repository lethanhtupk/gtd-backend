from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser, UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('fullname', 'photo_url', 'role')
