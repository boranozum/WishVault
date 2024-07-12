from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from base.mixins import PaginationMixin
from base.response import RestResponse


class BaseViewSet(
    PaginationMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    ordering = None

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return RestResponse(
            status=response.status_code,
            message="Retrieved successfully",
            content=response.data
        )


