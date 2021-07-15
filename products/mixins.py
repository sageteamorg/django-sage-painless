"""
Auto Generated mixins.py
You may need to change some parts
"""

from django.core.cache import cache


class ModelCacheMixin:
    """
    Mixin for models that adds filtering on cached queryset.
    CACHE_KEY,CACHED_RELATED_OBJECT are required class variables at the inheriting class
    CACHE_KEY:
        String - key name used for caching the queryset
    CACHED_RELATED_OBJECT:
        List - list of foreign key attributes for model that needs to be cached
    """

    @classmethod
    def get_all_from_cache(cls):
        """
        Returns all instances stored in cache
        :return: List of Model instances.
        """
        if not hasattr(cls, 'CACHE_KEY'):
            raise AttributeError("CACHE_KEY must be defined in {}".format(cls.__name__))

        if hasattr(cls, 'CACHED_RELATED_OBJECT'):
            queryset = cache.get_or_set(
                cls.CACHE_KEY,
                cls.objects.all().select_related(*cls.CACHED_RELATED_OBJECT),
            )
        else:
            queryset = cache.get_or_set(cls.CACHE_KEY, cls.objects.all())
        return list(queryset)

    @classmethod
    def filter_from_cache(cls, queryset=None, **kwargs):
        """
        Filters and returns Model instances from cache.
        It currently supports 2 types of filter
        1. Equality Filter - e.g id = 1 and name = 'test'
           filter_from_cache(id=1, name= 'test')
        2. In List Filter - e.g id in [1,2,3]
           filter_from_cache(id= [1,2,3])
        :param queryset: list of model instances that needs to be filtered.
                         If not present, filtering is done on all cached instances
        :param kwargs: dictionary containing filter property and values.
        :return: List containing Model objects
        """
        if not queryset:
            queryset = cls.get_all_from_cache()

        def filter_obj(obj):
            select = True  # boolean indicating if the item should be selected
            for filter_key, filter_value in kwargs.items():
                if isinstance(filter_value, list):
                    if getattr(obj, filter_key) not in filter_value:
                        select = False
                        break
                elif getattr(obj, filter_key) != filter_value:
                    select = False
                    break
            return select

        return list(filter(filter_obj, queryset))

    @classmethod
    def filter_related_from_cache(cls, queryset=None, **kwargs):
        """
        Filtering is based on model's foreign keys,
        which is set as CACHED_RELATED_OBJECT in model class.
        It currently supports 2 types of filter
        1. Equality Filter for foreign key's table- e.g id = 1 and name = 'test'
           filter_from_cache(foreign_key= {"name": "test", "id": 5})
        2. In List Filter for foreign key's table- e.g id in [1,2,3]
           filter_from_cache(foreign_key={'id': [1,2,3]})
        :param queryset: list of model instances that needs to be filtered.
        :param kwargs: dictionary containing filter property and values.
        :return: List containing Model objects
        """
        if not queryset:
            queryset = cls.get_all_from_cache()

        for foreign_key, related_filters in kwargs.items():
            related_objects_list = [getattr(obj, foreign_key) for obj in queryset]
            # Filtering related objects based related object's attribute filtes
            filtered_related_objects = cls.filter_from_cache(
                related_objects_list, **related_filters
            )
            # Filtering queryset based filtered related objects
            queryset = list(
                filter(
                    lambda x: getattr(x, foreign_key) in filtered_related_objects,
                    queryset,
                )
            )
        return queryset
