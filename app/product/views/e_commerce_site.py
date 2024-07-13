from account.models import GlobalPermission
from base.mixins import DestroyMixin, UpdateMixin, CreateMixin
from product.models import ECommerceSite
from product.permissions import ECommerceSitePermission
from product.serializers.e_commerce_site import ECommerceSiteSerializer
from base.views import BaseViewSet


class ECommerceSiteViewSet(
    DestroyMixin,
    UpdateMixin,
    CreateMixin,
    BaseViewSet,
):
    queryset = ECommerceSite.objects.all()
    serializer_class = ECommerceSiteSerializer
    ordering = 'name'
    search_fields = ['name']
    permission_classes = (ECommerceSitePermission,)
    permission_name = GlobalPermission.PERMISSION_COMMERCE_SITE_MANAGEMENT
