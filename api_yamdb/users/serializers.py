from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import MAX_LENGTH_USERNAME, User
from .validators import validate_username_not_prohibited


MAX_LENGTH_EMAIL = 254


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=(
            UnicodeUsernameValidator(), validate_username_not_prohibited),
    )
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL, required=True)

    def validate(self, data):
        super().validate(data)

        user_for_email = User.objects.filter(email=data['email']).first()
        user_for_username = User.objects.filter(
            username=data['username']).first()

        if user_for_username != user_for_email:
            error_msg = {}
            if user_for_username:
                error_msg['username'] = (
                    'Пользователь с таким username уже существует!')
            if user_for_email:
                error_msg['email'] = (
                    'Пользователь с таким email уже существует!')
            raise serializers.ValidationError(error_msg)
        return data


class UserObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=True,
        validators=(
            UnicodeUsernameValidator(), validate_username_not_prohibited),
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
