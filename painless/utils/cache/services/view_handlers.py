from django.http import Http404

from painless.utils.cache.services.cache_handlers import filter_from_cache


def get_object(self):
    """
    Get object from cache
    Must be replaced with `get_object()` method in viewsets
    """
    lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
    filter_kwargs = {
        self.lookup_field: self.kwargs[lookup_url_kwarg]
    }
    qs = filter_from_cache(self.queryset, **filter_kwargs)
    if len(qs) == 0:
        raise Http404('Not Found')
    obj = qs[0]
    return obj
