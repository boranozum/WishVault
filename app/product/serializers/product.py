from rest_framework import serializers

from base.serializers import BaseModelSerializer
from product.models import Product
from product.serializers.e_commerce_site import ECommerceSiteSerializer


class ProductSerializer(BaseModelSerializer):
    sold_at = ECommerceSiteSerializer(read_only=True)
    sold_at_id = serializers.IntegerField(write_only=True, required=False)
    cover_photo = serializers.ImageField(required=False)

    class Meta(BaseModelSerializer.Meta):
        model = Product
        fields = BaseModelSerializer.Meta.fields + [
            'name',
            'price',
            'rating',
            'sold_at',
            'sold_at_id',
            'cover_photo'
        ]
