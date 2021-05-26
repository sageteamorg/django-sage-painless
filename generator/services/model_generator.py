import yaml

from django.conf import settings

from generator.classes.field import Field
from generator.classes.model import Model
from generator.services.jinja_service import Jinja
from generator.services.pep8_service import Pep8


class ModelGenerator(Jinja, Pep8):

    FIELDS_KEYWORD = 'fields'
    TABLES_KEYWORD = 'tables'
    TYPE_KEYWORD = 'type'

    def __init__(self, app_label):
        self.app_label = app_label

    def load_diagram(self, diagram_path):
        """
        load db diagram
        """
        with open(diagram_path, 'r') as f:
            diagram = yaml.load_all(f.read(), Loader=yaml.FullLoader)
        return list(diagram)

    def get_table_fields(self, table, table_name):
        return table.get(table_name).get(self.FIELDS_KEYWORD)

    def extract_models(self, diagram):
        """
        extract models from yaml file
        """
        # TODO: Make field names dynamic
        models = list()
        for table in diagram[0].get(self.TABLES_KEYWORD):
            table_name = list(table.keys())[0]
            fields = self.get_table_fields(table, table_name)

            model = Model()
            model.name = table_name
            model_fields = list()

            for field in fields:
                model_field = Field()
                model_field.name = list(field.keys())[0]
                field_data = field.get(model_field.name)

                for data in field_data:
                    if self.TYPE_KEYWORD in list(data.keys()):
                        model_field.set_type(data.get(self.TYPE_KEYWORD))
                    else:
                        key = list(data.keys())[0]
                        value = data.get(key)
                        model_field.add_attribute(key, value)

                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models

    def generate_models(self, diagram_path):
        """
        store models in app_name/models.py
        """
        diagram = self.load_diagram(diagram_path)
        models = self.extract_models(diagram)
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/{self.app_label}/models.py',
            template_path=f'{settings.BASE_DIR}/generator/templates/models.txt',  # TODO: Should be dynamic
            data={
                'models': models
            }
        )

        self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/models.py')

        return True
