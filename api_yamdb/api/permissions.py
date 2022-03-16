from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class AdminOrReadOnly(BasePermission):
    """Админ, либо просто читает."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin or request.method in SAFE_METHODS:
            return True


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.user == obj.author
            or request.method in SAFE_METHODS
        ):
            return True
