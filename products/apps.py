"""
Auto Generated apps.py
Automatically generated with ❤️ by django-sage-painless
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self):
        import products.signals
    
