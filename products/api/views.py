"""
Auto Generated views.py
Automatically generated with ❤️ by django-sage-painless
"""

from django.http import Http404

from rest_framework.viewsets import ModelViewSet

# permission support
from rest_framework import permissions


# filter support
from django_filters.rest_framework import DjangoFilterBackend


# search support
from rest_framework.filters import SearchFilter


from products.models.category import Category

from products.models.product import Product

from products.models.discount import Discount

from products.api.serializers import (
    CategorySerializer,
    ProductSerializer,
    DiscountSerializer,

)


class CategoryViewset(ModelViewSet):
    """
    Category Viewset
    Auto generated
    """
    serializer_class = CategorySerializer
    
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = (permissions.AllowAny,)
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        'title', 'created', 'modified',
    ]
    filterset_fields = [
        'title', 'created', 'modified',
    ]
    
    model_class = Category

    def get_queryset(self):
        """
        get queryset from cache
        """
        return self.model_class.get_all_from_cache()

    def get_object(self):
        """
        get object from cache
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: int(
                self.kwargs[lookup_url_kwarg]) if self.kwargs[lookup_url_kwarg].isdigit() else None
        }
        qs = self.model_class.filter_from_cache(queryset, **filter_kwargs)
        if len(qs) == 0:
            raise Http404('Not Found')
        obj = qs[0]
        return obj
    

class ProductViewset(ModelViewSet):
    """
    Product Viewset
    Auto generated
    """
    serializer_class = ProductSerializer
    
    model_class = Product

    def get_queryset(self):
        """
        get queryset from cache
        """
        return self.model_class.get_all_from_cache()

    def get_object(self):
        """
        get object from cache
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: int(
                self.kwargs[lookup_url_kwarg]) if self.kwargs[lookup_url_kwarg].isdigit() else None
        }
        qs = self.model_class.filter_from_cache(queryset, **filter_kwargs)
        if len(qs) == 0:
            raise Http404('Not Found')
        obj = qs[0]
        return obj
    

class DiscountViewset(ModelViewSet):
    """
    Discount Viewset
    Auto generated
    """
    serializer_class = DiscountSerializer
    
    model_class = Discount

    def get_queryset(self):
        """
        get queryset from cache
        """
        return self.model_class.get_all_from_cache()

    def get_object(self):
        """
        get object from cache
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: int(
                self.kwargs[lookup_url_kwarg]) if self.kwargs[lookup_url_kwarg].isdigit() else None
        }
        qs = self.model_class.filter_from_cache(queryset, **filter_kwargs)
        if len(qs) == 0:
            raise Http404('Not Found')
        obj = qs[0]
        return obj
    
