from django.urls import include, path

from api.v1.urls import urlpatterns


urlpatterns = [
    path('v1/', include(urlpatterns)),
]
