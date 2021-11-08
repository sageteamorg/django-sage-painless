"""
django-sage-painless - Model Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractModelGenerator

# Helpers
from sage_painless.utils.file_service import FileService
from sage_painless.utils.timing_service import TimingService
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8

# Validators
from sage_painless.validators.setting_validator import SettingValidator

from sage_painless import templates


class ModelGenerator(AbstractModelGenerator, JinjaHandler, JsonHandler, Pep8, FileService, TimingService, GitSupport):
    """Read models data from a Json file and stream it to app_name/models.py"""
    MIXINS_TEMPLATE = 'mixins.jinja'
    SERVICES_TEMPLATE = 'services.jinja'
    MODELS_TEMPLATE = 'models.jinja'
    SIGNALS_TEMPLATE = 'signals.jinja'
    INIT_TEMPLATE = '__init__.jinja'
    APPS_TEMPLATE = 'apps.jinja'

    def __init__(self, *args, **kwargs):
        """init"""
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path: str, app_name: str, cache_support: bool = False, git_support: bool = False):
        """stream models to app_name/models/model_name.py
        generate signals, mixins, services
        templates:
            sage_painless/templates/models.jinja
            sage_painless/templates/signals.jinja
            sage_painless/templates/mixins.jinja
            sage_painless/templates/services.jinja
        """
        start_time = time.time()
        diagram = self.load_json(diagram_path)

        models_diagram = diagram.get(self.get_constant('APPS_KEYWORD')).get(app_name).get(
            self.get_constant('MODELS_KEYWORD'))  # get models data for current app
        models, signals = self.extract_models_and_signals(models_diagram)  # extract models and signals from diagram data

        # initialize
        self.create_app_if_not_exists(app_name)
        self.create_dir_for_app_if_not_exists('models', app_name)
        self.create_file_if_not_exists(f'{settings.BASE_DIR}/{app_name}/models/__init__.py')
        self.delete_file_if_exists(f'{settings.BASE_DIR}/{app_name}/models.py')
        if git_support:
            self.init_repo(settings.BASE_DIR)

        # mixins & services
        if cache_support:
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/mixins.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.MIXINS_TEMPLATE),
                data={
                    'cache_support': cache_support
                }
            )

            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/services.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.SERVICES_TEMPLATE),
                data={
                    'cache_support': cache_support
                }
            )

            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/mixins.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/services.py')
            if git_support:
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/services.py',
                    f'feat ({app_name}--services): Create cache service'
                )
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/mixins.py',
                    f'feat ({app_name}--mixins): Create cache mixin'
                )

        # validations
        if self.check_encryption_support(models):
            SettingValidator.validate_pgcrypto_config()

        # models
        for model in models:
            model_file_name = f'{model.name.lower()}.py'  # model file name is lower of model name (e.g Category
            # -> category.py)
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/models/{model_file_name}',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.MODELS_TEMPLATE),
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
            if git_support:
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/models/{model_file_name}',
                    f'feat ({app_name}--models): Create {model.name} model'
                )

        # signals
        if self.check_signal_support(models):
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/signals.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.SIGNALS_TEMPLATE),
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
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.INIT_TEMPLATE),
                data={
                    'app_name': app_name
                }
            )

            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/apps.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.APPS_TEMPLATE),
                data={
                    'app_name': app_name,
                    'signal_support': True
                }
            )

            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/signals.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/apps.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/__init__.py')
            if git_support:
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/signals.py',
                    f'feat ({app_name}--signals): Create model OneToOne signals'
                )
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/apps.py',
                    f'feat ({app_name}--signals): Add signals to apps.py'
                )
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/__init__.py',
                    f'feat ({app_name}--signals): Add signals to __init__'
                )

        elif cache_support:
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/signals.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.SIGNALS_TEMPLATE),
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
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.INIT_TEMPLATE),
                data={
                    'app_name': app_name
                }
            )

            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/apps.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.APPS_TEMPLATE),
                data={
                    'app_name': app_name,
                    'signal_support': True
                }
            )

            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/signals.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/apps.py')
            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/__init__.py')
            if git_support:
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/signals.py',
                    f'feat ({app_name}--signals): Create cache update signals'
                )
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/apps.py',
                    f'feat ({app_name}--signals): Add signals to apps.py'
                )
                self.commit_file(
                    f'{settings.BASE_DIR}/{app_name}/__init__.py',
                    f'feat ({app_name}--signals): Add signals to __init__'
                )
        end_time = time.time()
        return True, 'models generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
