"""
Auto Generated admin.py
You may need to change some parts
"""
from django.contrib import admin
from django.db.models import CharField, DateField, DateTimeField
from api.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User Admin
    Auto generated
    """
    list_display = [
        field.column for field in User._meta.get_fields() if type(field) == CharField
    ]

    list_filter = [
        field.column for field in User._meta.get_fields() if type(field) == DateField or type(field) == DateTimeField
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile Admin
    Auto generated
    """
    list_display = [
        field.column for field in Profile._meta.get_fields() if type(field) == CharField
    ]

    list_filter = [
        field.column for field in Profile._meta.get_fields() if type(field) == DateField or type(field) == DateTimeField
    ]
