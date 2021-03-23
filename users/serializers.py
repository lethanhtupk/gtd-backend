from rest_framework import serializers
from users.models import CustomUser, UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=70)
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    re_password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'fullname',
                  'is_verified', 'is_seller', 'password', 're_password', 'fullname')

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        if password != re_password:
            raise serializers.ValidationError(
                "The two password fields didn't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        return CustomUser.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
