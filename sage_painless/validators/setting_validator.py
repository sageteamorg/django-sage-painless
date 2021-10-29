"""
django-sage-painless - Settings Validator Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
from django.db import connection


class SettingValidator:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def validate_pgcrypto_config(cls):
        """validate database settings for encryption
        django-sage-encrypt just works in PostgreSQL
        check default db
        """
        default_vendor = connection.vendor
        if not default_vendor == 'postgresql':
            raise AssertionError('encryption just works on PostgreSQL.')
