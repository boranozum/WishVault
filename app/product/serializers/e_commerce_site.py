from rest_framework import serializers

from base.serializers import BaseModelSerializer
from product.models import ECommerceSite


class ECommerceSiteSerializer(BaseModelSerializer):
    site_logo = serializers.ImageField(required=False)
    scrape_map = serializers.JSONField(write_only=True, required=False)

    class Meta(BaseModelSerializer.Meta):
        model = ECommerceSite
        fields = BaseModelSerializer.Meta.fields + [
            'name',
            'base_url',
            'site_logo',
            'scrape_map'
        ]
