from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка разрешений для админа или на чтение."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated)  # добавить проверку на админа


class AdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Проверка разрешений для админа, модератора и автора."""

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user  # добавить проверку на админа и
            # модератора
        )
