"""
Auto Generated models.py
Automatically generated with ❤️ by django-sage-painless
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


# cache support
from products.mixins import ModelCacheMixin


class Category(models.Model, ModelCacheMixin):
    """
    Category Model
    Auto generated
    """
    
    CACHE_KEY = 'category'  # auto generated CACHE_KEY
    
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
        return f"Category {self.pk}" 

    class Meta:
        verbose_name = _("Category")  # auto generated verbose_name
        verbose_name_plural = _("Categories")
