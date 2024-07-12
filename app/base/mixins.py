import traceback

from django.http import Http404
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin

from base.response import RestResponse
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_204_NO_CONTENT


class CreateMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return RestResponse(
                status=response.status_code,
                message="Record created successfully",
                content=response.data
            )
        except:
            print(traceback.format_exc())
            return RestResponse(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to create record"
            )


class UpdateMixin(UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return RestResponse(
                status=response.status_code,
                message="Record updated successfully",
                content=response.data
            )
        except Http404:
            return RestResponse(
                status=HTTP_404_NOT_FOUND,
                message="No record found"
            )
        except Exception as e:
            print(traceback.format_exc())
            return RestResponse(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to update record"
            )


class DestroyMixin(DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return RestResponse(
                status=response.status_code,
                message="Record deleted successfully"
            )
        except Http404:
            return RestResponse(
                status=HTTP_404_NOT_FOUND,
                message="No record found"
            )
        except:
            print(traceback.format_exc())
            return RestResponse(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to delete record"
            )

    @action(detail=True, methods=['delete'], url_path='force_delete')
    def force_delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete(force=True)
        except self.model.DoesNotExist:
            return RestResponse(
                status=HTTP_404_NOT_FOUND,
                message="No record found"
            )

        return RestResponse(
            status=HTTP_204_NO_CONTENT,
            message="Record deleted successfully"
        )


class PaginationMixin:
    def paginated_action(self, request, serializer_class, queryset):
        page = self.paginate_queryset(queryset)

        if page is not None:
            params = request.query_params.copy()
            if ordering := getattr(self, "ordering"):
                params['default_ordering'] = ordering
            serializer = serializer_class(page, many=True)
            return RestResponse(
                message="",
                status=200,
                content={
                    'data': self.get_paginated_response(serializer.data).data,
                    'params': params,
                    'filter': {'param': 'filters', 'ops': []},
                    'ordering': {'param': 'ordering'},
                    'request_body': request.data
                }
            )

        return RestResponse(
            status=HTTP_400_BAD_REQUEST,
            message=""
        )


class MultiActionMixin:
    @action(detail=False, methods=['post'], url_path='update')
    def multi_update(self, request):
        pks = request.query_params.get("pks", "").split(",")
        if pks is None:
            return RestResponse(
                status=HTTP_400_BAD_REQUEST,
                message="No PKs provided"
            )

        queryset = self.filter_queryset(self.get_queryset().filter(pk__in=pks))
        if not queryset.exists():
            return RestResponse(
                status=HTTP_404_NOT_FOUND,
                message="No records found"
            )

        try:
            for instance in queryset:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        except:
            print(traceback.format_exc())
            return RestResponse(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to update records"
            )

        return RestResponse(
            message="Records updated successfully",
            content=self.get_serializer(queryset, many=True).data
        )

    @action(detail=False, methods=['delete'], url_path='delete')
    def multi_delete(self, request):
        pks = request.query_params.get("pks", "").split(",")
        if pks is None:
            return RestResponse(
                status=HTTP_400_BAD_REQUEST,
                message="No PKs provided"
            )

        queryset = self.filter_queryset(self.get_queryset().filter(pk__in=pks))
        if not queryset.exists():
            return RestResponse(
                status=HTTP_404_NOT_FOUND,
                message="No records found"
            )

        try:
            queryset.delete()
        except:
            print(traceback.format_exc())
            return RestResponse(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to delete records"
            )

        return RestResponse(
            status=HTTP_204_NO_CONTENT,
            message="Records deleted successfully"
        )