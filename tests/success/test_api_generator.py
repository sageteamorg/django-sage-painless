import os

from django.test import TestCase

from sage_painless.services.api_generator import APIGenerator
from sage_painless.utils.json_service import JsonHandler

from tests import fixtures


class TestAPIGenerator(TestCase):
    def setUp(self) -> None:
        self.json_handler = JsonHandler()
        self.app_name = 'products'
        self.api_generator = APIGenerator()
        self.diagram_path = os.path.abspath(fixtures.__file__).replace('__init__.py', 'product_fixture.json')
        self.diagram = self.json_handler.load_json(self.diagram_path).get('apps').get(self.app_name).get('models')

    def get_table_names(self):
        return self.diagram.keys()

    def get_table_field_names(self, table_name):
        return self.diagram.get(table_name).get('fields').keys()

    def test_extract_models(self):
        models = self.api_generator.extract_models(self.diagram)

        self.assertEqual(len(models), len(self.get_table_names()))

        for model in models:
            self.assertIn(model.name, self.get_table_names())
            for field in model.fields:
                self.assertIn(
                    field.name, self.get_table_field_names(model.name)
                )


