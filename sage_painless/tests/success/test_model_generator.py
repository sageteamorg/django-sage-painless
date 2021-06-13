import os

from django.test import TestCase
from django.conf import settings

from sage_painless.services.model_generator import ModelGenerator
from sage_painless.utils.json_service import JsonHandler

from sage_painless.classes.field import Field

from sage_painless.tests import diagrams


class TestModelGenerator(TestCase):
    def setUp(self) -> None:
        self.json_handler = JsonHandler()
        self.app_name = 'products'
        self.model_generator = ModelGenerator(self.app_name)
        self.diagram_path = os.path.abspath(diagrams.__file__).replace('__init__.py', 'product_diagram.json')
        self.diagram = self.json_handler.load_json(self.diagram_path)
        self.field = Field()
        self.field_types = self.field.field_types

    def get_table_names(self):
        return self.diagram.keys()

    def get_table_signals(self):
        signals = list()
        for table_name in self.diagram.keys():
            table = self.diagram.get(table_name)
            fields = self.model_generator.get_table_fields(table)
            for field_name in fields.keys():
                field_data = fields.get(field_name)
                for key in field_data.keys():
                    if key == self.model_generator.TYPE_KEYWORD:
                        if field_data.get(self.model_generator.TYPE_KEYWORD) == 'one2one':
                            signals.append(field_name)
        return signals

    def get_table_field_names(self, table_name):
        return self.diagram.get(table_name).get('fields').keys()

    def get_field_type(self, table_name, field_name):
        return self.diagram.get(table_name).get('fields').get(field_name).get('type')

    def get_field_attr_names(self, table_name, field_name):
        attrs = list(self.diagram.get(table_name).get('fields').get(field_name).keys())
        attrs.remove('type')
        return attrs

    def get_attr_value(self, table_name, field_name, attr_name):
        return self.diagram.get(table_name).get('fields').get(field_name).get(attr_name)

    def check_validator_support(self, models):
        for model in models:
            for field in model.fields:
                if len(field.validators) > 0:
                    return True

        return False

    def check_signal_support(self, models):
        for model in models:
            for field in model.fields:
                if field.type == 'OneToOneField':
                    return True

        return False

    def test_extract_models(self):
        """
        extract models from Json diagram
        """
        models, signals = self.model_generator.extract_models(self.diagram)

        self.assertEqual(len(models), len(self.get_table_names()))

        for model in models:
            self.assertIn(model.name, self.get_table_names())
            for field in model.fields:
                self.assertIn(
                    field.name, self.get_table_field_names(model.name)
                )
                self.assertEqual(
                    field.type, self.field_types.get(
                        self.get_field_type(
                            model.name,
                            field.name
                        )
                    ).get('type')
                )
                self.assertEqual(
                    len(field.attrs), len(self.get_field_attr_names(
                        model.name,
                        field.name
                    ))
                )
                for attribute in field.attrs:
                    self.assertIn(
                        attribute.key, self.get_field_attr_names(
                            model.name,
                            field.name
                        )
                    )
                    self.assertEqual(
                        attribute.value, self.get_attr_value(
                            model.name,
                            field.name,
                            attribute.key
                        )
                    )

        self.assertEqual(len(signals), len(self.get_table_signals()))

        for signal in signals:
            self.assertIn(signal.field, self.get_table_signals())
            self.assertIn(signal.model_a, self.get_table_names())
            self.assertEqual(signal.model_b, self.get_attr_value(signal.model_a, signal.field, 'to'))

    def test_check_validator_support(self):
        """
        check is there validator in models
        """
        models, signals = self.model_generator.extract_models(self.diagram)
        check_model_generator = self.model_generator.check_validator_support(models)
        check_test = self.check_validator_support(models)
        self.assertEqual(check_test, check_model_generator)

    def test_check_signal_support(self):
        """
        check need signal in models
        """
        models, signals = self.model_generator.extract_models(self.diagram)
        check_model_generator = self.model_generator.check_signal_support(models)
        check_test = self.check_signal_support(models)
        self.assertEqual(check_test, check_model_generator)
