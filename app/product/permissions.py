from base.permissions import BaseModelPermission


class ECommerceSitePermission(BaseModelPermission):
    def has_permission(self, request, view):
        if request.method in ["POST"] and not request.user.is_superuser:
            return False

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"] and not request.user.is_superuser:
            return False

        return True
