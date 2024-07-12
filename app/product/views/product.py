from base.views import BaseViewSet
from base.mixins import MultiActionMixin, DestroyMixin, UpdateMixin, CreateMixin
from product.models import Product
from product.serializers.product import ProductSerializer


class ProductViewSet(
    MultiActionMixin,
    DestroyMixin,
    UpdateMixin,
    CreateMixin,
    BaseViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering = 'created_at'

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

