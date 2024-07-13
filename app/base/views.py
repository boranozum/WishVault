from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from base.mixins import PaginationMixin, RetrieveMixin


class BaseViewSet(
    PaginationMixin,
    RetrieveMixin,
    ListModelMixin,
    GenericViewSet
):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]


