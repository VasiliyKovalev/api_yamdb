from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .filters import TitleFilter
from .viewsets import CategoryGenreViewSet
from .utils import send_confirmation_code
from .permissions import (
    IsAdminOnly, IsAdminOrReadOnly, IsAdminModeratorAuthorOrReadOnly)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    RegistrationSerializer, ReviewSerializer, TitleReadSerializer,
    TitleSerializer, UserObtainTokenSerializer, UserProfileSerializer,
    UserSerializer
)


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
        email = data['email']
        user, created = User.objects.get_or_create(
            username=data['username'], email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(confirmation_code, email)
        return Response(
            data,
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
                {'confirmation_code': ['Неверный код подтверждения!']},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""
    queryset = User.objects.all()
    permission_classes = (IsAdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.user.is_admin():
            return UserSerializer
        return UserProfileSerializer

    @action(
        detail=False,
        methods=('get', 'patch',),
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_me(self, request):
        serializer_class = self.get_serializer_class()
        if request.method == 'PATCH':
            serializer = serializer_class(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
