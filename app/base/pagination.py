from rest_framework import pagination
from rest_framework.pagination import _positive_int

from base.response import RestResponse


class Paginator(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return RestResponse(
            message="",
            content={
                "page": {
                    "size": {
                        "value": self.get_page_size(self.request),
                        "param": self.page_size_query_param,
                    },
                    "current": self.page.number,
                    "total": self.page.paginator.num_pages,
                    "param": self.page_query_param,
                },
                "count": self.page.paginator.count,
                "results": data,
            }
        )

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

