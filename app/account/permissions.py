from django.contrib.auth import get_user_model

from wishvault.settings import ADMIN_PASSWORD


def create_admin_user(**kwargs):
    user, _ = get_user_model().objects.update_or_create(
        id=0,
        defaults={
            "username": "admin",
            "is_superuser": True,
        }
    )

    user.set_password(ADMIN_PASSWORD)
    user.save()
