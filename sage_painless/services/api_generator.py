import os
import time

from django.conf import settings

from sage_painless.classes.field import Field
from sage_painless.classes.model import Model
from sage_painless.utils.file_service import FileService
from sage_painless.utils.git_service import GitSupport

from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8

from sage_painless import templates
from sage_painless.utils.timing_service import TimingService


class APIGenerator(
    JinjaHandler, JsonHandler, Pep8,
    FileService, TimingService, GitSupport
):
    """Generate API serializers & viewsets"""

    APPS_KEYWORD = 'apps'
    MODELS_KEYWORD = 'models'
    FIELDS_KEYWORD = 'fields'
    API_KEYWORD = 'api'
    API_DIR = 'api'
    STREAM_KEYWORD = 'stream'

    def __init__(self, *args, **kwargs):
        """init"""
        super().__init__(*args, **kwargs)

    def get_table_fields(self, table):
        """get fields"""
        return table.get(self.FIELDS_KEYWORD)

    def get_table_api(self, table):
        """get api"""
        return table.get(self.API_KEYWORD)

    def normalize_api_config(self, api_config):
        """get api config
        normalize api methods
        return api config
        """
        if api_config:
            if api_config.get('methods'):
                api_config['methods'] = [method.lower() for method in api_config.get('methods')]

        return api_config

    def extract_models(self, diagram):
        """extract models"""
        models = list()
        for table_name in diagram.keys():
            table = diagram.get(table_name)
            fields = self.get_table_fields(table)
            api_config = self.get_table_api(table)

            model = Model()
            model.name = table_name
            model.api_config = self.normalize_api_config(api_config)
            model_fields = list()

            for field_name in fields.keys():
                model_field = Field()
                model_field.name = field_name
                model_field.stream = fields.get(field_name).pop(self.STREAM_KEYWORD, False)  # video field streaming
                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models

    def add_urls_to_kernel(self):
        """TODO: add app urls to kernel"""
        pass

    def check_streaming_support(self, models):
        """check for streaming support in models"""
        for model in models:
            for field in model.fields:
                if field.stream:
                    return True

        return False

    def generate_api(self, diagram_path, cache_support=False, git_support=False):
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
        for app_name in diagram.get(self.APPS_KEYWORD).keys():
            models_diagram = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)  # get models data for current app
            models = self.extract_models(models_diagram)

            # initialization
            self.create_app_if_not_exists(app_name)
            self.create_dir_for_app_if_not_exists(self.API_DIR, app_name)
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
