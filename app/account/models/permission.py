from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


def create_permissions(**kwargs):
    for codename, name in GlobalPermission.PERMISSIONS:
        permission, created = GlobalPermission.objects.get_or_create(codename=codename, name=name)

    # Create superuser
    User = get_user_model()
    user, created = User.objects.get_or_create(
        id=0,
        defaults={
            "is_superuser": True,
            "username": "admin",
        },
    )
    user.set_password(settings.ADMIN_PASSWORD)
    user.save()


class GlobalPermissionManager(models.Manager):
    def get_queryset(self):
        return super(GlobalPermissionManager, self). \
            get_queryset().filter(content_type__model='global_permission')


class GlobalPermission(Permission):
    """A global permission, not attached to a model"""
    PERMISSION_PRODUCT_MANAGEMENT = "product_management"
    PERMISSION_COMMERCE_SITE_MANAGEMENT = "e_commerce_site_management"
    PERMISSION_USER_MANAGEMENT = "user_management"
    PERMISSION_PERMISSION_MANAGEMENT = "permission_management"
    PERMISSION_GROUP_MANAGEMENT = "group_management"
    PERMISSIONS = [
        (PERMISSION_PRODUCT_MANAGEMENT, "Product Management"),
        (PERMISSION_COMMERCE_SITE_MANAGEMENT, "E-Commerce Site Management"),
        (PERMISSION_USER_MANAGEMENT, "User Management"),
        (PERMISSION_PERMISSION_MANAGEMENT, "Permission Management"),
        (PERMISSION_GROUP_MANAGEMENT, "Group Management"),
    ]

    objects = GlobalPermissionManager()

    class Meta:
        proxy = True
        verbose_name = "global_permission"

    def save(self, *args, **kwargs):
        ct, created = ContentType.objects.get_or_create(
            model=self._meta.verbose_name, app_label=self._meta.app_label,
        )
        self.content_type = ct
        super(GlobalPermission, self).save(*args)
