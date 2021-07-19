import os
import time
from pathlib import Path

from django.conf import settings
from django.core import management

from sage_painless.classes.field import Field
from sage_painless.classes.model import Model
from sage_painless.classes.signal import Signal

from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8

from sage_painless import templates


class TestGenerator(JinjaHandler, JsonHandler, Pep8):
    """
    Create model/api tests for given diagram
    """

    APPS_KEYWORD = 'apps'
    MODELS_KEYWORD = 'models'
    FIELDS_KEYWORD = 'fields'
    TYPE_KEYWORD = 'type'
    VALIDATORS_KEYWORD = 'validators'
    FUNC_KEYWORD = 'func'
    ARG_KEYWORD = 'arg'
    TESTS_DIR = 'tests'

    def __init__(self):
        """init"""
        pass

    def get_table_fields(self, table):
        """get fields"""
        return table.get(self.FIELDS_KEYWORD)

    def extract_models(self, diagram):
        """extract models"""
        models = list()
        signals = list()
        for table_name in diagram.keys():
            table = diagram.get(table_name)
            fields = self.get_table_fields(table)

            model = Model()
            model.name = table_name
            model_fields = list()

            for field_name in fields.keys():
                model_field = Field()
                model_field.name = field_name
                field_data = fields.get(field_name)

                for key in field_data.keys():

                    if key == self.TYPE_KEYWORD:
                        model_field.set_type(field_data.get(self.TYPE_KEYWORD))

                        if model_field.type == 'OneToOneField':
                            signal = Signal()
                            signal.set_signal('post_save', table_name, field_data.get('to'), field_name)
                            signals.append(signal)

                    elif key == self.VALIDATORS_KEYWORD:
                        for validator in field_data.get(self.VALIDATORS_KEYWORD):
                            model_field.add_validator(validator.get(self.FUNC_KEYWORD), validator.get(self.ARG_KEYWORD))

                    else:
                        value = field_data.get(key)
                        model_field.add_attribute(key, value)

                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models, signals

    def create_dir_if_not_exists(self, directory, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{app_name}/{directory}')

    def create_file_if_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            file = Path(file_path)
            file.touch(exist_ok=True)

    def delete_file_if_exists(self, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

    def create_app_if_not_exists(self, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/'):
            management.call_command('startapp', app_name)

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def generate_tests(self, diagram_path):
        """stream tests to app_name/tests/*.py"""
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        for app_name in diagram.get(self.APPS_KEYWORD).keys():
            models_diagram = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)  # get models data for current app
            models, signals = self.extract_models(models_diagram)

            self.create_app_if_not_exists(app_name)
            self.create_dir_if_not_exists(self.TESTS_DIR, app_name)
            self.create_file_if_not_exists(f'{settings.BASE_DIR}/{app_name}/tests/__init__.py')
            self.delete_file_if_exists(f'{settings.BASE_DIR}/{app_name}/tests.py')

            # generate model tests
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/tests/test_model.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'test_model.txt'),
                data={
                    'app_name': app_name,
                    'models': models,
                    'signals': signals
                }
            )

            # generate api tests
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/tests/test_api.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'test_api.txt'),
                data={
                    'app_name': app_name,
                    'models': models
                }
            )

            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/tests/test_model.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/tests/test_api.py')
        end_time = time.time()
        return True, 'tests generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
