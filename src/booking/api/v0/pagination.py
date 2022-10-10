from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class DefaultPagePagination(PageNumberPagination):
    page_size = 6
    max_page_size = 1000
    page_size_query_param = 'page-size'

    def get_paginated_response(self, data):
        return Response(data, status.HTTP_200_OK, None, {
            'X-Pagination-Total': self.page.paginator.count,
            'X-Pagination-Per-Page': self.page.paginator.per_page,
            'X-Pagination-Page': self.page.number
        })
