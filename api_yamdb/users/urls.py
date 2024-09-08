from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserObtainTokenView, RegistrationView, UserViewSet


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')


auth_url = [
    path('signup/', RegistrationView.as_view()),
    path('token/', UserObtainTokenView.as_view(),),
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_url)),
]
