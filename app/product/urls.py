from rest_framework import routers

from product.views.e_commerce_site import ECommerceSiteViewSet
from product.views.product import ProductViewSet

router = routers.SimpleRouter()
router.register(r"e_commerce_site", ECommerceSiteViewSet, basename="e_commerce_site")
router.register(r"", ProductViewSet, basename="product")

urlpatterns = router.urls + []
