import os

from django.conf import settings

from generator.classes.field import Field
from generator.classes.model import Model
from generator.services.jinja_service import JinjaHandler
from generator.services.json_service import JsonHandler
from generator.services.pep8_service import Pep8


class APIGenerator(JinjaHandler, JsonHandler, Pep8):
    """
    Generate API serializers & viewsets
    """

    FIELDS_KEYWORD = 'fields'

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
                model_fields.append(model_field)

            model.fields = model_fields
            models.append(model)

        return models

    def create_dir_is_not_exists(self, directory):
        if not os.path.exists(f'{settings.BASE_DIR}/{self.app_label}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{self.app_label}/{directory}')

    def generate_api(self, diagram_path):
        """
        stream serializers to app_name/api/serializers.py
        stream viewsets to app_name/api/views.py
        """
        diagram = self.load_json(diagram_path)
        models = self.extract_models(diagram)

        self.create_dir_is_not_exists('api')

        # stream to serializers.py
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/{self.app_label}/api/serializers.py',
            template_path=f'{settings.BASE_DIR}/generator/templates/serializers.txt',
            data={
                'app_name': self.app_label,
                'models': models,
            }
        )

        # stream to views.py
        pass

        self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/api/serializers.py')

        return True, 'Generated successfully'
