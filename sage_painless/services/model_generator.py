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

class ModelGenerator(JinjaHandler, JsonHandler, Pep8):
    """Read models data from a Json file and stream it to app_name/models.py"""

    MODELS_KEYWORD = 'models'
    APPS_KEYWORD = 'apps'
    FIELDS_KEYWORD = 'fields'
    TYPE_KEYWORD = 'type'
    ENCRYPTED_KEYWORD = 'encrypt'
    STREAM_KEYWORD = 'stream'
    VALIDATORS_KEYWORD = 'validators'
    FUNC_KEYWORD = 'func'
    ARG_KEYWORD = 'arg'

    def __init__(self):
        """init"""
        pass

    def get_table_fields(self, table):
        """extract fields"""
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

                # Encrypt
                model_field.encrypted = field_data.pop(self.ENCRYPTED_KEYWORD, False)  # field encryption
                model_field.stream = field_data.pop(self.STREAM_KEYWORD, False)  # video field streaming

                for key in field_data.keys():
                    # Type
                    if key == self.TYPE_KEYWORD:
                        model_field.set_type(field_data.get(self.TYPE_KEYWORD))  # set type of Field (CharField, etc)

                        # if field is one2one create Signal
                        if model_field.type == 'OneToOneField':
                            signal = Signal()
                            signal.set_signal('post_save', table_name, field_data.get('to'), field_name)
                            signals.append(signal)

                    # Validator
                    elif key == self.VALIDATORS_KEYWORD:
                        for validator in field_data.get(self.VALIDATORS_KEYWORD):
                            model_field.add_validator(validator.get(self.FUNC_KEYWORD), validator.get(self.ARG_KEYWORD))

                    # Attributes
                    else:
                        value = field_data.get(key)
                        model_field.add_attribute(key, value)

                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models, signals

    def check_validator_support(self, models):
        """check models have validator"""
        for model in models:
            for field in model.fields:
                if len(field.validators) > 0:
                    return True

        return False

    def check_signal_support(self, models):
        """check models have one2one"""
        for model in models:
            for field in model.fields:
                if field.type == 'OneToOneField':
                    return True

        return False

    def check_encryption_support(self, models):
        """check models have encrypted field"""
        for model in models:
            for field in model.fields:
                if field.encrypted:
                    return True

        return False

    def get_fk_model_names(self, models):
        """check models have fk,m2m,one2one,... and return model names"""
        model_names = list()
        for model in models:
            for field in model.fields:
                if field.type in ['ManyToManyField', 'OneToOneField', 'ForeignKey']:
                    model_names.append(field.get_attribute('to'))

        return model_names

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

    def generate_models(self, diagram_path, cache_support=False):
        """stream models to app_name/models.py"""
        start_time = time.time()
        diagram = self.load_json(diagram_path)

        for app_name in diagram.get(self.APPS_KEYWORD).keys():
            models_diagram = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)  # get models data for current app
            models, signals = self.extract_models(models_diagram)  # extract models and signals from diagram data

            # initialize
            self.create_app_if_not_exists(app_name)
            self.create_dir_if_not_exists('models', app_name)
            self.create_file_if_not_exists(f'{settings.BASE_DIR}/{app_name}/models/__init__.py')
            self.delete_file_if_exists(f'{settings.BASE_DIR}/{app_name}/models.py')

            # mixins & services
            if cache_support:
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/mixins.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'mixins.txt'),
                    data={
                        'cache_support': cache_support
                    }
                )
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/services.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'services.txt'),
                    data={
                        'cache_support': cache_support
                    }
                )
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/mixins.py')
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/services.py')

            # models
            for model in models:
                model_file_name = f'{model.name.lower()}.py'  # model file name is lower of model name (e.g Category -> category.py)
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/models/{model_file_name}',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'models.txt'),
                    data={
                        'app_name': app_name,
                        'models': [model],
                        'validator_support': self.check_validator_support([model]),
                        'cache_support': cache_support,
                        'fk_models': self.get_fk_model_names([model]),
                        'encrypt_support': self.check_encryption_support([model])
                    }
                )
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/models/{model_file_name}')

            # signals
            if self.check_signal_support(models):
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/signals.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'signals.txt'),
                    data={
                        'app_name': app_name,
                        'models': models,
                        'signals': signals,
                        'signal_support': True,
                        'cache_support': cache_support
                    }
                )
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/__init__.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', '__init__.txt'),
                    data={
                        'app_name': app_name
                    }
                )
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/apps.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'apps.txt'),
                    data={
                        'app_name': app_name,
                        'signal_support': True
                    }
                )
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/signals.py')
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/apps.py')
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/__init__.py')

            elif cache_support:
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/signals.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'signals.txt'),
                    data={
                        'app_name': app_name,
                        'models': models,
                        'signals': signals,
                        'signal_support': True,
                        'cache_support': cache_support
                    }
                )
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/__init__.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', '__init__.txt'),
                    data={
                        'app_name': app_name
                    }
                )
                self.stream_to_template(
                    output_path=f'{settings.BASE_DIR}/{app_name}/apps.py',
                    template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'apps.txt'),
                    data={
                        'app_name': app_name,
                        'signal_support': True
                    }
                )
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/signals.py')
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/apps.py')
                self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/__init__.py')
        end_time = time.time()
        return True, 'models generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
