import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractAPIGenerator

# Helpers
from sage_painless.utils.file_service import FileService
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class APIGenerator(AbstractAPIGenerator, JinjaHandler, JsonHandler, Pep8, FileService, TimingService, GitSupport):
    """Generate API serializers & viewsets"""

    def __init__(self, *args, **kwargs):
        """init"""
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path, cache_support=False, git_support=False):
        """
        stream serializers to app_name/api/serializers.py
        stream viewsets to app_name/api/views.py
        stream urls to app_name/api/urls.py
        template:
            sage_painless/templates/serializers.txt
            sage_painless/templates/views.txt
            sage_painless/templates/urls.txt
        """
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        for app_name in diagram.get(self.get_constant('APPS_KEYWORD')).keys():
            models_diagram = diagram.get(
                self.get_constant('APPS_KEYWORD')).get(app_name).get(self.get_constant('MODELS_KEYWORD'))  # get models data for current app
            models = self.extract_models(models_diagram)

            # initialization
            self.create_app_if_not_exists(app_name)
            self.create_dir_for_app_if_not_exists(self.get_constant('API_DIR'), app_name)
            if git_support:
                self.init_repo(settings.BASE_DIR)

            # stream to serializers.py
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/api/serializers.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'serializers.txt'),
                data={
                    'app_name': app_name,
                    'models': models
                }
            )

            # stream to views.py
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/api/views.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'views.txt'),
                data={
                    'app_name': app_name,
                    'models': models,
                    'cache_support': cache_support
                }
            )

            # stream to urls.py
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/api/urls.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'urls.txt'),
                data={
                    'app_name': app_name,
                    'models': models,
                    'streaming_support': self.check_streaming_support(models)
                }
            )

            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/api/serializers.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/api/views.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/api/urls.py')
            if git_support:
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/api/serializers.py',
                    f'feat ({app_name}--serializers): Create serializers'
                )
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/api/views.py',
                    f'feat ({app_name}--views): Create API views'
                )
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/api/urls.py',
                    f'feat ({app_name}--urls): Add views to urls.py'
                )

        end_time = time.time()
        return True, 'API generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
