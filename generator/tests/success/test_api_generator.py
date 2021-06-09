from django.test import TestCase
from django.conf import settings

from generator.services.api_generator import APIGenerator
from generator.utils.json_service import JsonHandler


class TestAPIGenerator(TestCase):
    def setUp(self) -> None:
        self.json_handler = JsonHandler()
        self.app_name = 'products'
        self.api_generator = APIGenerator(self.app_name)
        self.diagram_path = settings.BASE_DIR + '/generator/tests/diagrams/product_diagram.json'
        self.diagram = self.json_handler.load_json(self.diagram_path)

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


