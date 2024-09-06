from django.urls import include, path, re_path

from .views import (
    UserDetail, UserList, UserProfile, UserObtainTokenView, RegistrationView,)


auth_url = [
    path('signup/', RegistrationView.as_view()),
    path('token/', UserObtainTokenView.as_view(),),
]

users_url = [
    path('', UserList.as_view()),
    path('me/', UserProfile.as_view()),
    re_path(r'(?P<username>[\w.@+-]+)/', UserDetail.as_view()),
]


urlpatterns = [
    path('users/', include(users_url)),
    path('auth/', include(auth_url)),
]
