import operator

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from painless.utils.cache.services.cache_handlers import filter_related_from_cache, filter_from_cache


class CacheFilterBackend(DjangoFilterBackend):
    """
    Integrated with cache
    filter foreign_key/attribute from cache
    """

    def get_filterset_fields(self, view):
        return getattr(view, 'filterset_fields', None)

    def filter_queryset(self, request, queryset, view):
        """
        Filter queryset from cache
        """

        filter_kwargs = {}
        for param in request.query_params:
            for field in self.get_filterset_fields(view):
                if param.startswith(field):
                    sub_fields = field.split('__')
                    length = len(sub_fields)
                    for i in range(length):
                        try:
                            filter_kwargs[sub_fields[i]] = {sub_fields[i + 1]: None}
                        except IndexError:
                            filter_kwargs[sub_fields[i - 1]][sub_fields[i]] = request.query_params[param]

        return filter_related_from_cache(queryset, **filter_kwargs)


class CacheSearchBackend(SearchFilter):
    """
    Integrated with cache
    search in cache via `contains` operator
    """
    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        filter_kwargs = {}
        for field in search_fields:
            sub_fields = field.split('__')
            length = len(sub_fields)
            for i in range(length):
                try:
                    filter_kwargs[sub_fields[i]] = {sub_fields[i + 1]: None}
                except IndexError:
                    if i == 0:
                        filter_kwargs[sub_fields[i]] = search_terms[i]
                    else:
                        filter_kwargs[sub_fields[i - 1]][sub_fields[i]] = search_terms[i]

        queryset = filter_from_cache(queryset, operator_=operator.contains, **filter_kwargs)

        return queryset
