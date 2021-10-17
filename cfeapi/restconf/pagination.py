from rest_framework import pagination

class CFEAPIPagination(pagination.LimitOffsetPagination):  # PageNumberPagination):
    page_size  =  5
    default_limit = 1
    max_limit  =  2
    # limit_query_param = 'lim'