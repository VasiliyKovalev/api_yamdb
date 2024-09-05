from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

# from api.permissions import AdminOrReadOnly


class CategoryGenreViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    # permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
