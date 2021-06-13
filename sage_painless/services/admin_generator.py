import os

from django.apps import apps
from django.conf import settings

from sage_painless.classes.admin import Admin

from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8

from sage_painless import templates


class AdminGenerator(JinjaHandler, JsonHandler, Pep8):

    ADMIN_KEYWORD = 'admin'
    TYPE_KEYWORD = 'type'

    def __init__(self, app_label):
        self.app_label = app_label

    def get_app_models(self, app_name):
        """
        extract models from app
        """
        return [model.__name__ for model in list(apps.get_app_config(app_name).get_models())]

    def get_diagram_models(self, diagram):
        """
        extract models from diagram
        """
        return list(diagram.keys())

    def validate_diagram(self, diagram):
        """
        check diagram models with app models if any difference return False
        """
        app_models = self.get_app_models(self.app_label)
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
        """
        extract admin attributes from json file
        """
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

    def generate(self, diagram_path):
        """
        generate admin.py for given app
        """
        diagram = self.load_json(diagram_path)
        check, message = self.validate_diagram(diagram)
        if check:
            admins = self.extract_admin(diagram)
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/{self.app_label}/admin.py',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'admin.txt'),  # TODO: Should be dynamic
                data={
                    'app_name': self.app_label,
                    'admins': admins,
                }
            )

            self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/admin.py')

            return True, 'Admin Generated Successfully. Changes are in this file:\nadmin.py\n'
        else:
            return False, f'models.py is not match with diagram differences : {message}'

