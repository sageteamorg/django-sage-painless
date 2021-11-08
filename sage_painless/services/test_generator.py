"""
django-sage-painless - Test Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractTestGenerator

# Helpers
from sage_painless.utils.file_service import FileService
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class TestGenerator(AbstractTestGenerator, JinjaHandler, JsonHandler, Pep8, FileService, TimingService, GitSupport):
    """Generate model/api tests for given diagram"""
    TEST_TEMPLATE = 'test.jinja'

    def __init__(self, *args, **kwargs):
        """init"""
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path: str, app_name: str, git_support: bool = False):
        """stream tests to app_name/tests/test_model_name.py
        template:
            sage_painless/templates/test.jinja
        """
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        if git_support:
            self.init_repo(settings.BASE_DIR)

        models_diagram = diagram.get(
            self.get_constant('APPS_KEYWORD')).get(app_name).get(
            self.get_constant('MODELS_KEYWORD'))  # get models data for current app
        models, signals = self.extract_models(models_diagram)

        self.create_app_if_not_exists(app_name)
        self.create_dir_for_app_if_not_exists(self.get_constant('TESTS_DIR'), app_name)
        self.create_file_if_not_exists(f'{settings.BASE_DIR}/{app_name}/tests/__init__.py')
        self.delete_file_if_exists(f'{settings.BASE_DIR}/{app_name}/tests.py')

        for model in models:
            # generate model tests
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/tests/test_{model.name.lower()}.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.TEST_TEMPLATE),
                data={
                    'app_name': app_name,
                    'models': models,
                    'model': model,
                    'signals': self.filter_signals_for_model(signals, model),
                    'stream': self.check_streaming_support([model])
                }
            )
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/tests/test_{model.name.lower()}.py')
            if git_support:
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/tests/test_{model.name.lower()}.py',
                    f'test ({app_name}--{model.name.lower()}): Test model & API'
                )
        end_time = time.time()
        return True, 'tests generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
