from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import MAX_LENGTH_USERNAME, User
from .utils import validate_username_not_me


class RegistrationSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_not_me),
    )
    email = serializers.EmailField(required=True)

    def validate(self, data):
        super().validate(data)
        username = data['username']
        email = data['email']
        user = User.objects.filter(username=username, email=email)

        if user.exists():
            return data
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': 'Пользователь с таким username уже существует!'}
            )
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Пользователь с таким email уже существует!'}
            )
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserObtainTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_not_me),
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
