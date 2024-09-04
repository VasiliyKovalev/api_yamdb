from django.urls import include, path, re_path

from .views import UserDetail, UserList, UserProfile, MyTokenView


auth_url = [
    # path('auth/signup/', ),
    path('token/', MyTokenView.as_view(), name='token_obtain_pair'),
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
