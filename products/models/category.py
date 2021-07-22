"""
Auto Generated models.py
You may need to change some parts
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


# cache support
from products.mixins import ModelCacheMixin


# encrypt support
from sage_encrypt.services.encrypt import encrypt_field


class Category(models.Model, ModelCacheMixin):
    """
    Category Model
    Auto generated
    """
    
    CACHE_KEY = 'category'
    
    title = encrypt_field(models.CharField(
             max_length=255,
             unique=True,
             
    ))
    
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
        verbose_name_plural = _("Categories")
