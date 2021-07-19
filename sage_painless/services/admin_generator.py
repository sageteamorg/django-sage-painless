import os
import time

from django.apps import apps
from django.conf import settings
from django.core import management

from sage_painless.classes.admin import Admin

from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8

from sage_painless import templates

class AdminGenerator(JinjaHandler, JsonHandler, Pep8):

    ADMIN_KEYWORD = 'admin'
    MODELS_KEYWORD = 'models'
    APPS_KEYWORD = 'apps'
    TYPE_KEYWORD = 'type'

    def __init__(self):
        """init"""
        pass

    def get_app_models(self, app_name):
        """extract models from app"""
        return [model.__name__ for model in list(apps.get_app_config(app_name).get_models())]

    def get_diagram_models(self, diagram):
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
        return table.get(self.ADMIN_KEYWORD)

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

    def create_app_if_not_exists(self, app_name):
        if not os.path.exists(f'{settings.BASE_DIR}/{app_name}/'):
            management.call_command('startapp', app_name)

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def generate(self, diagram_path):
        """generate admin.py for given app"""
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        for app_name in diagram.get(self.APPS_KEYWORD).keys():
            models_diagram = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)  # get models data for current app
            admins = self.extract_admin(models_diagram)

            self.create_app_if_not_exists(app_name)

            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{app_name}/admin.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'admin.txt'),
                data={
                    'app_name': app_name,
                    'admins': admins,
                }
            )

            self.fix_pep8(f'{settings.BASE_DIR}/{app_name}/admin.py')
        end_time = time.time()
        return True, 'admin generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))

