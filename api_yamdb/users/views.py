from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from api.utils import response_405_not_put
from .models import User
from .utils import generate_code, send_confirmation_code
from .permissions import IsAdminOnly
from .serializers import (
    UserObtainTokenSerializer, UserSerializer,
    RegistrationSerializer, UserProfileSerializer)


class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data['username']
        email = data['email']
        confirmation_code = generate_code()
        send_confirmation_code(confirmation_code, email)
        user = User.objects.filter(username=data['username'], email=email)
        if user.exists():
            user.update(confirmation_code=confirmation_code)
            return Response(data, status=status.HTTP_200_OK)
        elif User.objects.filter(username=username).exists():
            return Response(
                {'username': 'Пользователь с таким username уже существует!'},
                status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email).exists():
            return Response(
                {'email': 'Пользователь с таким email уже существует!'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(
                confirmation_code=confirmation_code,
            )
            return Response(data, status=status.HTTP_200_OK)


class UserObtainTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] != user.confirmation_code:
            return Response(
                {'confirmation_code': 'Неверный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def put(self, request, *args, **kwargs):
        return response_405_not_put()


class UserProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(User, username=self.request.user.username)

    def put(self, request, *args, **kwargs):
        return response_405_not_put()
