from django.contrib.auth.models import User
from rest_framework import generics, permissions

from catapp.models import Cat


# customized permission for Registered users only, also can use the  default permission (IsAuthenticated)
class RegisteredUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(User.objects.filter(pk=request.user.id))


# User can only update or delete one of his instance
class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner.id == request.user.id
