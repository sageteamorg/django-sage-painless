import os
from pathlib import Path

from django.conf import settings

from sage_painless.classes.field import Field
from sage_painless.classes.model import Model
from sage_painless.classes.signal import Signal

from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8

from sage_painless import templates

class ModelGenerator(JinjaHandler, JsonHandler, Pep8):
    """
    Read models data from a Json file and stream it to app_name/models.py
    """

    FIELDS_KEYWORD = 'fields'
    TYPE_KEYWORD = 'type'
    VALIDATORS_KEYWORD = 'validators'
    FUNC_KEYWORD = 'func'
    ARG_KEYWORD = 'arg'

    def __init__(self, app_label):
        self.app_label = app_label

    def get_table_fields(self, table):
        """
        extract fields
        """
        return table.get(self.FIELDS_KEYWORD)

    def extract_models(self, diagram):
        """
        extract models
        """
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

    def check_validator_support(self, models):
        """
        check models have validator
        """
        for model in models:
            for field in model.fields:
                if len(field.validators) > 0:
                    return True

        return False

    def check_signal_support(self, models):
        """
        check models have one2one
        """
        for model in models:
            for field in model.fields:
                if field.type == 'OneToOneField':
                    return True

        return False

    def get_fk_model_names(self, models):
        """
        check models have fk,m2m,one2one,... and return model names
        """
        model_names = list()
        for model in models:
            for field in model.fields:
                if field.type in ['ManyToManyField', 'OneToOneField', 'ForeignKey']:
                    model_names.append(field.get_attribute('to'))

        return model_names

    def create_dir_is_not_exists(self, directory):
        if not os.path.exists(f'{settings.BASE_DIR}/{self.app_label}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{self.app_label}/{directory}')

    def create_file_is_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            file = Path(file_path)
            file.touch(exist_ok=True)

    def delete_file_is_exists(self, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

    def generate_models(self, diagram_path, cache_support=False):
        """
        stream models to app_name/models.py
        """
        diagram = self.load_json(diagram_path)
        models, signals = self.extract_models(diagram)

        # initialize
        self.create_dir_is_not_exists('models')
        self.create_file_is_not_exists(f'{settings.BASE_DIR}/{self.app_label}/models/__init__.py')
        self.delete_file_is_exists(f'{settings.BASE_DIR}/{self.app_label}/models.py')

        # mixins & services
        if cache_support:
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/mixins.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'mixins.txt'),
                data={
                    'cache_support': cache_support
                }
            )
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/services.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'services.txt'),
                data={
                    'cache_support': cache_support
                }
            )
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/mixins.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/services.py')

        # models
        for model in models:
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/models/{model.name.lower()}.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'models.txt'),
                data={
                    'app_name': self.app_label,
                    'models': [model],
                    'validator_support': self.check_validator_support([model]),
                    'cache_support': cache_support,
                    'fk_models': self.get_fk_model_names([model])
                }
            )
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/models/{model.name.lower()}.py')

        # signals
        if self.check_signal_support(models):
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/signals.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'signals.txt'),
                data={
                    'app_name': self.app_label,
                    'models': models,
                    'signals': signals,
                    'signal_support': True,
                    'cache_support': cache_support
                }
            )
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/__init__.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', '__init__.txt'),
                data={
                    'app_name': self.app_label
                }
            )
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/apps.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'apps.txt'),
                data={
                    'app_name': self.app_label,
                    'signal_support': True
                }
            )
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/signals.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/apps.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/__init__.py')

        elif cache_support:
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/signals.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'signals.txt'),
                data={
                    'app_name': self.app_label,
                    'models': models,
                    'signals': signals,
                    'signal_support': True,
                    'cache_support': cache_support
                }
            )
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/__init__.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', '__init__.txt'),
                data={
                    'app_name': self.app_label
                }
            )
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/apps.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'apps.txt'),
                data={
                    'app_name': self.app_label,
                    'signal_support': True
                }
            )
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/signals.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/apps.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/__init__.py')

        return True, 'Models Generated Successfully.'
