import os
import time

from django.conf import settings
from django.core import management

from sage_painless.classes.field import Field
from sage_painless.classes.model import Model

from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8

from sage_painless import templates

class APIGenerator(JinjaHandler, JsonHandler, Pep8):
    """
    Generate API serializers & viewsets
    """

    APPS_KEYWORD = 'apps'
    MODELS_KEYWORD = 'models'
    FIELDS_KEYWORD = 'fields'
    API_KEYWORD = 'api'
    API_DIR = 'api'
    STREAM_KEYWORD = 'stream'

    def __init__(self):
        """init"""
        pass

    def get_table_fields(self, table):
        """get fields"""
        return table.get(self.FIELDS_KEYWORD)

    def get_table_api(self, table):
        """get api"""
        return table.get(self.API_KEYWORD)

    def normalize_api_config(self, api_config):
        """
        get api config
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

    def create_dir_if_not_exists(self, directory, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{app_name}/{directory}')

    def create_app_if_not_exists(self, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/'):
            management.call_command('startapp', app_name)

    def add_urls_to_kernel(self):
        """TODO: add app urls to kernel"""
        pass

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def check_streaming_support(self, models):
        """check for streaming support in models"""
        for model in models:
            for field in model.fields:
                if field.stream:
                    return True

        return False

    def generate_api(self, diagram_path, cache_support=False):
        """
        stream serializers to app_name/api/serializers.py
        stream viewsets to app_name/api/views.py
        stream urls to app_name/api/urls.py
        """
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        for app_name in diagram.get(self.APPS_KEYWORD).keys():
            models_diagram = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)  # get models data for current app
            models = self.extract_models(models_diagram)

            self.create_app_if_not_exists(app_name)
            self.create_dir_if_not_exists(self.API_DIR, app_name)

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

        end_time = time.time()
        return True, 'API generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
