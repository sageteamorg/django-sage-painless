from django.conf import settings

from generator.classes.field import Field
from generator.classes.model import Model

from generator.services.jinja_service import JinjaHandler
from generator.services.json_service import JsonHandler
from generator.services.pep8_service import Pep8


class ModelGenerator(JinjaHandler, JsonHandler, Pep8):
    """
    Read models data from a Json file and stream it to app_name/models.py
    """

    FIELDS_KEYWORD = 'fields'
    TYPE_KEYWORD = 'type'

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
                    else:
                        value = field_data.get(key)
                        model_field.add_attribute(key, value)

                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models

    def generate_models(self, diagram_path):
        """
        stream models to app_name/models.py
        """
        diagram = self.load_json(diagram_path)
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
