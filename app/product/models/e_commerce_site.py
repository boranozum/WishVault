from django.db import models

from base.models import AbstractBaseModel


class ECommerceSite(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(null=True)
    site_logo = models.ImageField(null=True, upload_to="site_logo/")

    def __str__(self):
        return f"{self.name} - {self.base_url}"
