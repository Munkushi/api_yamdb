from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.user == obj.author
            or request.method in permissions.SAFE_METHODS
        ):
            return True
