"""
Auto Generated signals.py
You may need to change some parts
"""

from django.db.models import signals


from products.models.category import Category

from products.models.product import Product

from products.models.discount import Discount

from products.services import clear_cache_for_model


def category_clear_cache(sender, **kwargs):
    clear_cache_for_model(sender.CACHE_KEY)


signals.post_save.connect(category_clear_cache, sender=Category)
signals.pre_delete.connect(category_clear_cache, sender=Category)


def product_clear_cache(sender, **kwargs):
    clear_cache_for_model(sender.CACHE_KEY)


signals.post_save.connect(product_clear_cache, sender=Product)
signals.pre_delete.connect(product_clear_cache, sender=Product)


def discount_clear_cache(sender, **kwargs):
    clear_cache_for_model(sender.CACHE_KEY)


signals.post_save.connect(discount_clear_cache, sender=Discount)
signals.pre_delete.connect(discount_clear_cache, sender=Discount)
