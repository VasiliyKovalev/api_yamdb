from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from .models import User
from .permissions import IsAdminOnly
from .utils import send_confirmation_code
from .serializers import (
    UserObtainTokenSerializer, UserSerializer,
    RegistrationSerializer, UserProfileSerializer)


class RegistrationView(APIView):
    """
    Вьюсет для регистрации пользователя.
    Высылает код подтверждения для получения токена.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data['username']
        email = data['email']

        try:
            user = User.objects.get(username=username, email=email)
        except ObjectDoesNotExist:
            serializer.save()
            user = User.objects.get(username=username, email=email)
        finally:
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_code(confirmation_code, email)
            return Response(
                {'username': username, 'email': email},
                status=status.HTTP_200_OK
            )


class UserObtainTokenView(APIView):
    """Вьюсет для получения JWT-токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']

        if not default_token_generator.check_token(
            user, confirmation_code
        ):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User"""
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.user.is_admin():
            return UserSerializer
        return UserProfileSerializer

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
