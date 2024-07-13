from rest_framework.permissions import BasePermission

from account.models import GlobalPermission


def grant_permission_to_user(user, *permission_names):
    user.user_permissions.add(*GlobalPermission.objects.filter(codename__in=permission_names))


class IsAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_active and request.user.is_authenticated


class BaseModelPermission(IsAuthenticatedPermission):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        if hasattr(view, 'permission_name') and view.permission_name:
            if request.user.is_superuser:
                return True

            return request.user.has_perm(f"account.{view.permission_name}")

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.created_by == request.user
