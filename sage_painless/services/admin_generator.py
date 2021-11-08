"""
django-sage-painless - Admin Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractAdminGenerator

# Helpers
from sage_painless.utils.file_service import FileService
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class AdminGenerator(AbstractAdminGenerator, JinjaHandler, JsonHandler, Pep8, FileService, TimingService, GitSupport):
    """Generate admin.py for apps from given diagram"""
    ADMIN_TEMPLATE = 'admin.jinja'

    def __init__(self, *args, **kwargs):
        """init"""
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path: str, app_name: str, git_support: bool = False):
        """generate admin.py
        template:
            sage_painless/templates/admin.jinja
        """
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        if git_support:
            self.init_repo(settings.BASE_DIR)
        models_diagram = diagram.get(
            self.get_constant('APPS_KEYWORD')).get(app_name).get(
            self.get_constant('MODELS_KEYWORD'))  # get models data for current app
        admins = self.extract_admin(models_diagram)

        self.create_app_if_not_exists(app_name)

        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/{app_name}/admin.py',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.ADMIN_TEMPLATE),
            data={
                'app_name': app_name,
                'admins': admins,
            }
        )
        self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/admin.py')
        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/{app_name}/admin.py',
                f'feat ({app_name}--admin): Add models to admin.py'
            )
        end_time = time.time()
        return True, 'admin generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
