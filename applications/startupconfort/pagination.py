from rest_framework.pagination import PageNumberPagination


class DateResultsSetPagination(PageNumberPagination):
    page_size = 24
    max_page_size = 24
