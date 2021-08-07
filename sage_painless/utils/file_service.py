import os
from pathlib import Path

from django.conf import settings
from django.core import management


class FileService:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_app_if_not_exists(self, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/'):
            management.call_command('startapp', app_name)

    def create_dir_if_not_exists(self, directory):
        if not os.path.exists(f'{settings.BASE_DIR}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{directory}')

    def create_file_if_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            file = Path(file_path)
            file.touch(exist_ok=True)

    def delete_file_if_exists(self, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

    def create_dir_for_app_if_not_exists(self, directory, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{app_name}/{directory}')
