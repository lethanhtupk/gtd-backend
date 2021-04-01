from django.core import paginator
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'paging': {
                'total': self.page.paginator.count,
                'per_page': self.page.paginator.per_page,
                'current_page': self.page.number,
                'last_page': self.page.paginator.num_pages,
                'from': self.page.start_index(),
                'to': self.page.end_index()
            },
            'data': data
        })
