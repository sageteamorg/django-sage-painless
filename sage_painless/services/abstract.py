"""
django-sage-painless - Abstract Generator Classes

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
from pathlib import Path

import django
from django.apps import apps
from django.conf import settings

from sage_painless.classes.admin import Admin
from sage_painless.classes.field import Field
from sage_painless.classes.model import Model
from sage_painless.classes.signal import Signal
from sage_painless.services.base import BaseGenerator
from sage_painless.services.constants import GeneratorConstants


class AbstractModelGenerator(BaseGenerator, GeneratorConstants):
    """Abstract Model Generator"""

    @classmethod
    def get_fk_model_names(cls, models: [Model]):
        """check models have fk,m2m,one2one,... and return model names"""
        model_names = list()
        for model in models:
            for field in model.fields:
                if field.type in ['ManyToManyField', 'OneToOneField', 'ForeignKey']:
                    model_names.append(field.get_attribute('to'))
        return model_names

    @classmethod
    def check_encryption_support(cls, models: [Model]):
        """check models have encrypted field"""
        for model in models:
            for field in model.fields:
                if field.encrypted:
                    return True
        return False

    @classmethod
    def check_validator_support(cls, models: [Model]):
        """check models have validator"""
        for model in models:
            for field in model.fields:
                if len(field.validators) > 0:
                    return True
        return False

    @classmethod
    def check_signal_support(cls, models: [Model]):
        """check models have one2one"""
        for model in models:
            for field in model.fields:
                if field.type == 'OneToOneField':
                    return True
        return False

    def get_table_fields(self, table: dict):
        """extract fields from table dict"""
        return table.get(self.get_constant('FIELDS_KEYWORD'))

    def extract_models_and_signals(self, diagram: dict):
        """extract Model & Signal objects from given diagram (dict)
        return ([Model], [Signal])
        """
        models = list()
        signals = list()
        for table_name in diagram.keys():
            table = diagram.get(table_name)  # get each table content
            fields = self.get_table_fields(table)  # get table fields

            model = Model()  # initialize Model object (will set attrs)
            model.name = table_name
            model_fields = list()

            for field_name in fields.keys():  # iterate in model fields
                model_field = Field()
                model_field.name = field_name
                field_data = fields.get(field_name)

                # Encrypt
                model_field.encrypted = field_data.pop(
                    self.get_constant('ENCRYPTED_KEYWORD'), False)  # field encryption

                # Streaming
                model_field.stream = field_data.pop(
                    self.get_constant('STREAM_KEYWORD'), False)  # video field streaming

                for key in field_data.keys():
                    # Field type
                    if key == self.get_constant('TYPE_KEYWORD'):
                        model_field.set_type(
                            field_data.get(self.get_constant('TYPE_KEYWORD')))  # set type of Field (CharField, etc)

                        # if field is one2one create Signal
                        if model_field.type == 'OneToOneField':
                            signal = Signal()
                            signal.set_signal('post_save', table_name, field_data.get('to'), field_name)
                            signals.append(signal)

                    # Validator
                    elif key == self.get_constant('VALIDATORS_KEYWORD'):
                        for validator in field_data.get(self.get_constant('VALIDATORS_KEYWORD')):
                            model_field.add_validator(
                                validator.get(
                                    self.get_constant('FUNC_KEYWORD')), validator.get(self.get_constant('ARG_KEYWORD')))

                    # Attributes
                    else:
                        value = field_data.get(key)
                        model_field.add_attribute(key, value)

                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models, signals


class AbstractAdminGenerator(BaseGenerator, GeneratorConstants):
    """Abstract Admin Generator"""

    @classmethod
    def get_app_models(cls, app_name):
        """extract models from app"""
        return [model.__name__ for model in list(apps.get_app_config(app_name).get_models())]

    @classmethod
    def get_diagram_models(cls, diagram):
        """extract models from diagram"""
        return list(diagram.keys())

    def validate_diagram(self, diagram, app_name):
        """check diagram models with app models if any difference return False"""
        app_models = self.get_app_models(app_name)
        diagram_models = self.get_diagram_models(diagram)
        differences = list(set(diagram_models).symmetric_difference(set(app_models)))
        if len(differences) == 0:
            message = True, 'Success'
        else:
            message = False, differences

        return message

    def get_table_admin(self, table):
        return table.get(self.get_constant('ADMIN_KEYWORD'))

    def extract_admin(self, diagram):
        """extract admin attributes from json file"""
        admins = list()
        for table_name in diagram.keys():
            table = diagram.get(table_name)
            admin_data = self.get_table_admin(table)

            admin = Admin()
            admin.model = table_name
            for key in admin_data.keys():
                value = admin_data.get(key)
                setattr(admin, key, value)

            admins.append(admin)

        return admins


class AbstractAPIGenerator(BaseGenerator, GeneratorConstants):
    """Abstract API Generator"""

    permission_routing = {
        'any': 'AllowAny',
        'auth': 'IsAuthenticated',
        'auth_or_read': 'IsAuthenticatedOrReadOnly',
        'admin': 'IsAdminUser'
    }

    def normalize_api_config(self, api_config):
        """get api config
        normalize api methods
        normalize api permissions
        return api config
        """
        if api_config:
            if api_config.get(self.get_constant('METHODS_KEYWORD')):
                api_config[self.get_constant('METHODS_KEYWORD')] = [
                    method.lower() for method in api_config.get(self.get_constant('METHODS_KEYWORD'))]

            if api_config.get(self.get_constant('PERMISSION_KEYWORD')):
                api_config[self.get_constant('PERMISSION_KEYWORD')] = self.permission_routing.get(
                    api_config.get(self.get_constant('PERMISSION_KEYWORD'))
                )
        else:
            api_config = dict()
        return api_config

    @classmethod
    def check_streaming_support(cls, models):
        """check for streaming support in models"""
        for model in models:
            for field in model.fields:
                if field.stream:
                    return True

        return False

    def check_permission_support(self, models):
        """check for permission support in api config"""
        for model in models:
            if model.api_config.get(self.get_constant('PERMISSION_KEYWORD')):
                return True

        return False

    def check_filter_support(self, models):
        """check for filter support in api config"""
        for model in models:
            if model.api_config.get(self.get_constant('FILTER_KEYWORD')):
                return True

        return False

    def check_search_support(self, models):
        """check for search support in api config"""
        for model in models:
            if model.api_config.get(self.get_constant('SEARCH_KEYWORD')):
                return True

        return False

    def get_table_fields(self, table):
        """get fields"""
        return table.get(self.get_constant('FIELDS_KEYWORD'))

    def get_table_api(self, table):
        """get api"""
        return table.get(self.get_constant('API_KEYWORD'))

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
                field_data = fields.get(field_name)
                model_field = Field()
                model_field.name = field_name
                model_field.set_type(
                    field_data.get(self.get_constant('TYPE_KEYWORD')))  # set type of Field (CharField, etc)
                model_field.stream = fields.get(field_name).pop(self.STREAM_KEYWORD, False)  # video field streaming
                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models


class AbstractTestGenerator(BaseGenerator, GeneratorConstants):
    """Abstract Test Generator"""

    @classmethod
    def filter_signals_for_model(cls, signals, model):
        """return the signals with model_a model"""
        filtered = list()
        for signal in signals:
            if signal.model_a == model.name:
                filtered.append(signal)
        return filtered

    @classmethod
    def normalize_api_config(cls, api_config):
        """
        get api config
        normalize api methods
        return api config
        """
        if api_config:
            if api_config.get('methods'):
                api_config['methods'] = [method.lower() for method in api_config.get('methods')]

        return api_config

    @classmethod
    def check_streaming_support(cls, models):
        """check for streaming support in models"""
        for model in models:
            for field in model.fields:
                if field.stream:
                    return True

        return False

    def get_table_fields(self, table):
        """get fields"""
        return table.get(self.get_constant('FIELDS_KEYWORD'))

    def get_table_api(self, table):
        """get api"""
        return table.get(self.get_constant('API_KEYWORD'))

    def extract_models(self, diagram):
        """extract models"""
        models = list()
        signals = list()
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
                model_field.stream = fields.get(field_name).pop(
                    self.get_constant('STREAM_KEYWORD'), False)  # video field streaming
                field_data = fields.get(field_name)

                for key in field_data.keys():

                    if key == self.TYPE_KEYWORD:
                        model_field.set_type(field_data.get(self.get_constant('TYPE_KEYWORD')))

                        if model_field.type == 'OneToOneField':
                            signal = Signal()
                            signal.set_signal('post_save', table_name, field_data.get('to'), field_name)
                            signals.append(signal)

                    elif key == self.get_constant('VALIDATORS_KEYWORD'):
                        for validator in field_data.get(self.get_constant('VALIDATORS_KEYWORD')):
                            model_field.add_validator(
                                validator.get(self.get_constant('FUNC_KEYWORD')),
                                validator.get(self.get_constant('ARG_KEYWORD')))

                    else:
                        value = field_data.get(key)
                        model_field.add_attribute(key, value)

                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models, signals


class AbstractDockerGenerator(BaseGenerator, GeneratorConstants):
    """Abstract Docker Generator"""

    @classmethod
    def get_kernel_name(cls):
        """get project kernel name"""
        return settings.SETTINGS_MODULE.split('.')[0]

    def extract_deploy_config(self, diagram):
        """extract deploy deploy config from diagram"""
        deploy = diagram.get(self.get_constant('DEPLOY_KEYWORD'))
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy

    def get_staticfiles_dir(self):
        """get staticfiles dir
        `web` is container name
        """
        directory = settings.STATIC_ROOT
        if not directory:
            raise SystemError('STATIC_ROOT should be set in your settings')
        return directory.replace(self.get_kernel_name(), 'web')

    def get_mediafiles_dir(self):
        """get mediafiles dir
        `web` is container name
        """
        directory = settings.MEDIA_ROOT
        if not directory:
            raise SystemError('MEDIA_ROOT should be set in your settings')
        return directory.replace(self.get_kernel_name(), 'web')


class AbstractGunicornGenerator(BaseGenerator, GeneratorConstants):
    """Abstract Gunicorn Generator"""

    def extract_gunicorn_config(self, diagram):
        """extract gunicorn config from diagram json"""
        deploy = diagram.get(self.get_constant('DEPLOY_KEYWORD'))
        if not deploy:
            return {}
        return deploy.get(self.get_constant('GUNICORN_KEYWORD'))


class AbstractReadMeGenerator(BaseGenerator, GeneratorConstants):
    """Abstract ReadMe Generator"""

    @classmethod
    def get_built_in_app_names(cls):
        """django built-in apps"""
        return [app.verbose_name for app in apps.get_app_configs() if app.name.startswith('django.')]

    @classmethod
    def get_installed_module_names(cls):
        """extra installed modules to setting"""
        return [app.verbose_name for app in apps.get_app_configs() if not app.name.startswith('django.')]

    @classmethod
    def get_project_name(cls):
        """get project root name"""
        base_dir = settings.BASE_DIR
        return base_dir.name if hasattr(base_dir, 'name') else base_dir

    @classmethod
    def get_project_version(cls):
        """get current project version if set"""
        return getattr(settings, 'VERSION', '1.0.0')

    @classmethod
    def get_django_version(cls):
        """get current Django version"""
        return django.get_version()

    @classmethod
    def merge(cls, list_a: list, list_b: list):
        """merge 2 lists"""
        return list(set(list_a + list_b))

    @classmethod
    def has_docker_support(cls):
        """is project dockerized"""
        compose_file_yml = Path(f'{settings.BASE_DIR}/docker-compose.yml')
        compose_file_yaml = Path(f'{settings.BASE_DIR}/docker-compose.yaml')

        if compose_file_yml.is_file() or compose_file_yaml.is_file():
            return True

        return False

    def make_tree(self, dir_path: Path, prefix: str = ''):
        """create project root tree structure"""
        contents = list(dir_path.iterdir())
        pointers = [self.get_constant('TEE')] * (len(contents) - 1) + [self.get_constant('LAST')]

        for pointer, path in zip(pointers, contents):
            if path.name not in self.get_constant('IGNORE_DIRS'):
                yield prefix + pointer + path.name
                if path.is_dir():
                    extension = self.get_constant('BRANCH') if pointer == self.get_constant(
                        'TEE') else self.get_constant('SPACE')
                    yield from self.make_tree(path, prefix=prefix + extension)


class AbstractToxGenerator(BaseGenerator, GeneratorConstants):
    """Abstract Tox Generator"""

    @classmethod
    def get_app_names(cls):
        """get diagram app names"""
        return [app.name for app in apps.get_app_configs() if not app.name.startswith('django.')]

    @classmethod
    def get_kernel_name(cls):
        """get project kernel name"""
        return settings.SETTINGS_MODULE.split('.')[0]

    @classmethod
    def parse_requirements(cls, requirements):
        with open(requirements) as f:
            return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

    def extract_tox_config(self, diagram):
        """extract tox config from diagram json"""
        deploy = diagram.get(self.get_constant('DEPLOY_KEYWORD'))
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy.get(self.get_constant('TOX_KEYWORD'))


class AbstractUWSGIGenerator(BaseGenerator, GeneratorConstants):
    """Abstract UWSGI Generator"""

    def extract_uwsgi_config(self, diagram):
        """extract uwsgi config from diagram json"""
        deploy = diagram.get(self.get_constant('DEPLOY_KEYWORD'))
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy.get(self.get_constant('UWSGI_KEYWORD'))


class AbstractNiginxGenerator(BaseGenerator, GeneratorConstants):
    """Abstract Nginx Generator"""

    @classmethod
    def get_static_files_dir(cls):
        """get from django setting"""
        if hasattr(settings, 'STATIC_ROOT'):
            return getattr(settings, 'STATIC_ROOT')
        else:
            raise AssertionError('You need to set STATIC_ROOT in django settings')

    @classmethod
    def get_media_files_dir(cls):
        """get from django setting"""
        if hasattr(settings, 'MEDIA_ROOT'):
            return getattr(settings, 'MEDIA_ROOT')
        else:
            raise AssertionError('You need to set MEDIA_ROOT in django settings')

