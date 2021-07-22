"""
Auto Generated models.py
You may need to change some parts
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
