"""
Auto Generated admin.py
You may need to change some parts
"""
from django.contrib import admin
from products.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category Admin
    Auto generated
    """
    list_display = ['title', 'created', 'modified']

    list_filter = ['created', 'modified']

    search_fields = ['title']

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product Admin
    Auto generated
    """
    list_display = ['title', 'price', 'category']

    list_filter = ['created', 'modified']

    search_fields = ['title', 'description']

    raw_id_fields = ['category']

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Discount Admin
    Auto generated
    """
    list_display = ['discount', 'product', 'created', 'modified']

    list_filter = ['created', 'modified']

    raw_id_fields = ['product']

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True
