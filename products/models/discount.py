"""
Auto Generated models.py
You may need to change some parts
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


# cache support
from products.mixins import ModelCacheMixin


from products.models.product import Product


class Discount(models.Model, ModelCacheMixin):
    """
    Discount Model
    Auto generated
    """
    
    CACHE_KEY = 'discount'
    
    product = models.ForeignKey(
             to=Product,
             related_name='discounts',
             on_delete=models.CASCADE,
             
    )
    
    discount = models.IntegerField(
             
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
