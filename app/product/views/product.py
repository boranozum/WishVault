from account.models import GlobalPermission
from base.response import RestResponse
from base.views import BaseViewSet
from base.mixins import MultiActionMixin, DestroyMixin, UpdateMixin, CreateMixin
from product.filters import ProductFilter
from product.models import Product
from product.serializers.product import ProductSerializer
from rest_framework.decorators import action

from product.utils.product_parser import ProductParser


class ProductViewSet(
    MultiActionMixin,
    DestroyMixin,
    UpdateMixin,
    CreateMixin,
    BaseViewSet
):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price', 'rating', 'created_at']
    ordering = ['name']
    permission_name = GlobalPermission.PERMISSION_PRODUCT_MANAGEMENT

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()

        return Product.objects.filter(
            created_by=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        try:
            existing_instance = Product.all_objects.get(
                name=request.data.get('name'),
                is_deleted=True,
            )
            existing_instance.delete(force=True)
        except Product.DoesNotExist:
            pass

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['POST'], url_path='parse')
    def parse(self, request):
        product = ProductParser().parse(request.data.get('url'))
        name = product.pop("name")
        sold_at_id = product.pop("sold_at_id")
        obj = None
        if name or sold_at_id:
            obj, _ = Product.objects.update_or_create(
                name=name,
                sold_at_id=sold_at_id,
                defaults=product
            )

        return RestResponse(
            message='Parsed',
            content=obj
        )


