from rest_framework import serializers

from base.serializers import BaseModelSerializer
from product.models import ECommerceSite


class ECommerceSiteSerializer(BaseModelSerializer):
    site_logo = serializers.ImageField(required=False)

    class Meta(BaseModelSerializer.Meta):
        model = ECommerceSite
