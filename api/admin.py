"""
Auto Generated admin.py
You may need to change some parts
"""
from django.contrib import admin
from api.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User Admin
    Auto generated
    """
    list_display = ['username', 'first_name', 'last_name']

    list_filter = ['is_active', 'last_login']

    search_fields = ['username']

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile Admin
    Auto generated
    """
    list_display = ['user']

    raw_id_fields = ['user']

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True
