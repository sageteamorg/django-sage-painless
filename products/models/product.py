"""
Auto Generated models.py
Automatically generated with ❤️ by django-sage-painless
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


# cache support
from products.mixins import ModelCacheMixin


from products.models.category import Category


class Product(models.Model, ModelCacheMixin):
    """
    Product Model
    Auto generated
    """
    
    CACHE_KEY = 'product'  # auto generated CACHE_KEY
    
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
        return f"Product {self.pk}" 

    class Meta:
        verbose_name = _("Product")  # auto generated verbose_name
        verbose_name_plural = _("Products")
