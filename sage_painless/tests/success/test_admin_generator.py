import os

from django.test import TestCase
from django.apps import apps
from django.conf import settings

from sage_painless.classes.admin import Admin
from sage_painless.services.admin_generator import AdminGenerator
from sage_painless.utils.json_service import JsonHandler

from sage_painless.tests import diagrams


class TestAdminGenerator(TestCase):
    def setUp(self) -> None:
        self.json_handler = JsonHandler()
        self.app_name = 'products'
        self.admin_generator = AdminGenerator(self.app_name)
        self.diagram_path = os.path.abspath(diagrams.__file__).replace('__init__.py', 'product_diagram.json')
        self.diagram = self.json_handler.load_json(self.diagram_path)

    def get_diagram_admins(self, diagram):
        admins = list()
        for table_name in diagram.keys():
            table = diagram.get(table_name)
            admin_data = self.admin_generator.get_table_admin(table)

            admin = Admin()
            admin.model = table_name
            for key in admin_data.keys():
                value = admin_data.get(key)
                setattr(admin, key, value)

            admins.append(admin)

        return admins

    def check_field_value(self, list1, list2, field):
        for item in list1:
            for item2 in list2:
                if getattr(item, field) == getattr(item2, field):
                    return True

        return False

    def open_generated_file(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
        return data

    def get_obj_properties(self, obj):
        return vars(obj)

    def test_get_app_models(self):
        generator_models = self.admin_generator.get_app_models(self.app_name)
        app_models = [model.__name__ for model in list(apps.get_app_config(self.app_name).get_models())]
        self.assertListEqual(generator_models, app_models)

    def test_validate_diagram(self):
        app_models = self.admin_generator.get_app_models(self.app_name)
        diagram_models = self.admin_generator.get_diagram_models(self.diagram)
        check, diff = self.admin_generator.validate_diagram(self.diagram)
        test_diff = list(set(diagram_models).symmetric_difference(set(app_models)))
        if len(test_diff) == 0:
            self.assertTrue(check)
        else:
            self.assertFalse(check)
            self.assertListEqual(diff, test_diff)

    def test_extract_admin(self):
        admins = self.admin_generator.extract_admin(self.diagram)
        test_admins = self.get_diagram_admins(self.diagram)

        self.assertEqual(len(admins), len(test_admins))
        self.assertTrue(self.check_field_value(admins, test_admins, 'model'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'list_display'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'list_filter'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'search_fields'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'raw_id_fields'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'filter_horizontal'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'filter_vertical'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'has_add_permission'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'has_change_permission'))
        self.assertTrue(self.check_field_value(admins, test_admins, 'has_delete_permission'))

    def test_stream_to_jinja(self):
        admins = self.admin_generator.extract_admin(self.diagram)
        self.admin_generator.generate(self.diagram_path)
        admin_data = self.open_generated_file(f'{settings.BASE_DIR}/{self.app_name}/admin.py')
        for admin in admins:
            for prop in self.get_obj_properties(admin):
                if getattr(admin, prop):
                    self.assertTrue(getattr(admin, prop), admin_data)
