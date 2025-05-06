from rest_framework.pagination import LimitOffsetPagination


class OptionalLimitOffsetPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        if ('limit' in request.query_params
                and 'offset' in request.query_params):
            return super().paginate_queryset(queryset, request, view)
        return None
