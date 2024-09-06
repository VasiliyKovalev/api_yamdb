from rest_framework import serializers

from .models import User


class UsernameNotMeSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя!')
        return value


class RegistrationSerializer(UsernameNotMeSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=150, required=True
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class UserSerializer(UsernameNotMeSerializer):

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


class UserProfileSerializer(UsernameNotMeSerializer):

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
