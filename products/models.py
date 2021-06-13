"""
Auto Generated models.py
You may need to change some parts
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


from django.db.models import signals


from django.core.cache import cache
from django.db.models import signals


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
            raise AttributeError(
                "CACHE_KEY must be defined in {}".format(
                    cls.__name__))

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
            related_objects_list = [
                getattr(obj, foreign_key) for obj in queryset]
            # Filtering related objects based related object's attribute filtes
            filtered_related_objects = cls.filter_from_cache(
                related_objects_list, **related_filters
            )
            # Filtering queryset based filtered related objects
            queryset = list(
                filter(
                    lambda x: getattr(
                        x,
                        foreign_key) in filtered_related_objects,
                    queryset,
                ))
        return queryset


def clear_cache_for_model(cache_key: str):
    """
    removes all caches of this model
    """
    keys = cache.keys(f'*{cache_key}*')
    cache.delete_many(keys)


class Category(models.Model, ModelCacheMixin):
    """
    Category Model
    Auto generated
    """

    CACHE_KEY = 'category'

    title = models.CharField(
        max_length=255,
        unique=True,

    )

    created = models.DateTimeField(
        auto_now_add=True,

    )

    modified = models.DateTimeField(
        auto_now=True,

    )

    def __str__(self):
        return f"Category {self.pk}"  # you may change this section

    class Meta:
        verbose_name = _("Category")  # auto generated verbose_name
        verbose_name_plural = _("Categorys")


def category_clear_cache(sender, **kwargs):
    clear_cache_for_model(sender.CACHE_KEY)


signals.post_save.connect(category_clear_cache, sender=Category)
signals.pre_delete.connect(category_clear_cache, sender=Category)


class Product(models.Model, ModelCacheMixin):
    """
    Product Model
    Auto generated
    """

    CACHE_KEY = 'product'

    title = models.CharField(
        max_length=255,

    )

    description = models.CharField(
        max_length=255,

    )

    price = models.IntegerField(

    )

    category = models.ForeignKey(
        to=Category,
        related_name='products',
        on_delete=models.CASCADE,

    )

    created = models.DateTimeField(
        auto_now_add=True,

    )

    modified = models.DateTimeField(
        auto_now=True,

    )

    def __str__(self):
        return f"Product {self.pk}"  # you may change this section

    class Meta:
        verbose_name = _("Product")  # auto generated verbose_name
        verbose_name_plural = _("Products")


def product_clear_cache(sender, **kwargs):
    clear_cache_for_model(sender.CACHE_KEY)


signals.post_save.connect(product_clear_cache, sender=Product)
signals.pre_delete.connect(product_clear_cache, sender=Product)


class Discount(models.Model, ModelCacheMixin):
    """
    Discount Model
    Auto generated
    """

    CACHE_KEY = 'discount'

    product = models.OneToOneField(
        to=Product,
        related_name='discounts',
        on_delete=models.CASCADE,

    )

    discount = models.IntegerField(
        default=0,

    )

    created = models.DateTimeField(
        auto_now_add=True,

    )

    modified = models.DateTimeField(
        auto_now=True,

    )

    def __str__(self):
        return f"Discount {self.pk}"  # you may change this section

    class Meta:
        verbose_name = _("Discount")  # auto generated verbose_name
        verbose_name_plural = _("Discounts")


def discount_clear_cache(sender, **kwargs):
    clear_cache_for_model(sender.CACHE_KEY)


signals.post_save.connect(discount_clear_cache, sender=Discount)
signals.pre_delete.connect(discount_clear_cache, sender=Discount)


# Signals

def product_post_save(sender, instance, created, **kwargs):
    if created:
        Discount.objects.create(product=instance)


signals.post_save.connect(product_post_save, sender=Product)
