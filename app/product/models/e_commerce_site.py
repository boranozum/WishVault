import urllib.parse

from django.db import models

from base.models import AbstractBaseModel


class ECommerceSiteManager(models.Manager):
    def get_from_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        return self.get_queryset().filter(base_url__icontains=parsed_url.netloc)


class ECommerceSite(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(null=True)
    site_logo = models.ImageField(null=True, upload_to="site_logo/")
    scrape_map = models.JSONField(null=True)

    objects = ECommerceSiteManager()

    def __str__(self):
        return f"{self.name} - {self.base_url}"
