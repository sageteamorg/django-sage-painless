"""
Auto Generated admin.py
You may need to change some parts
"""
from django.contrib import admin
from articles.models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Article Admin
    Auto generated
    """
    list_display = ['title', 'created', 'updated']

    list_filter = ['created', 'updated', 'options']

    search_fields = ['title', 'body']

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True
