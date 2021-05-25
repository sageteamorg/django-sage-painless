import subprocess

import yaml
from django.conf import settings

from generator.classes.field import Field
from generator.classes.model import Model
from generator.services.jinja_service import stream_to_template


class ModelGenerator:
    def __init__(self, app_label):
        self.app_label = app_label

    def fix_pep8(self, file_path):
        """
        fix pep8
        """
        subprocess.run(
            [
                'autopep8',
                '--in-place',
                '--aggressive',
                '--aggressive',
                file_path
            ]
        )

    def load_diagram(self, diagram_path):
        """
        load db diagram
        """
        with open(diagram_path, 'r') as f:
            diagram = yaml.load_all(f.read(), Loader=yaml.FullLoader)
        return list(diagram)

    def prepare_to_generate(self, diagram):
        """
        prepare data to generate model


        [
        {
        'User':
            {'fields': [
                {
                    'username': [{'type': 'CharField'}, {'unique': True}]
                },
                {
                    'password': [{'type': 'CharField'}]
                },
                {
                    'first_name': [{'type': 'CharField'}]
                },
                {
                    'last_name': [{'type': 'CharField'}]
                },
                {
                    'is_active': [{'type': 'BooleanField'}]
                },
                {
                    'last_login': [{'type': 'DateTimeField'}]
                }],
                'meta': [
                    {
                        'verbose_name': 'User'
                    },
                    {
                        'verbose_name_plural': 'Users'
                    }
                    ]
                }
            }
        ]
        """
        # TODO: Make field names dynamic
        models = list()
        for table in diagram[0].get('tables'):
            table_name = list(table.keys())[0]
            fields = table.get(table_name).get('fields')
            meta = table.get('meta')
            model = Model()
            model.name = table_name
            model_fields = list()
            for field in fields:
                model_field = Field()
                model_field.name = list(field.keys())[0]
                field_data = field.get(model_field.name)
                for data in field_data:
                    if 'type' in list(data.keys()):
                        model_field.set_type(data.get('type'))
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
        models = self.prepare_to_generate(diagram)
        stream_to_template(
            output_path=f'{settings.BASE_DIR}/{self.app_label}/models.py',
            template_path=f'{settings.BASE_DIR}/generator/templates/models.txt',  # TODO: Should be dynamic
            data={
                'models': models
            }
        )

        self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/models.py')

        return True
