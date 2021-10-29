"""
django-sage-painless - File Handling Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
from pathlib import Path

from django.conf import settings
from django.core import management


class FileService:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_app_if_not_exists(cls, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/'):
            management.call_command('startapp', app_name)

    @classmethod
    def create_dir_if_not_exists(cls, directory):
        if not os.path.exists(f'{settings.BASE_DIR}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{directory}')

    @classmethod
    def create_file_if_not_exists(cls, file_path):
        if not os.path.isfile(file_path):
            file = Path(file_path)
            file.touch(exist_ok=True)

    @classmethod
    def delete_file_if_exists(cls, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

    @classmethod
    def create_dir_for_app_if_not_exists(cls, directory, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{app_name}/{directory}')
