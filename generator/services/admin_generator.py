from django.apps import apps
from django.conf import settings

from generator.services.jinja_service import Jinja
from generator.services.pep8_service import Pep8


class AdminGenerator(Jinja, Pep8):
    def __init__(self, app_label):
        self.app_label = app_label

    def get_app_models(self, app_name):
        return [model.__name__ for model in list(apps.get_app_config(app_name).get_models())]

    def generate(self):
        """
        generate admin.py for given app
        """
        models = self.get_app_models(self.app_label)
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/{self.app_label}/admin.py',
            template_path=f'{settings.BASE_DIR}/generator/templates/admin.txt',  # TODO: Should be dynamic
            data={
                'app_name': self.app_label,
                'models': models,
            }
        )

        self.fix_pep8(f'{settings.BASE_DIR}/{self.app_label}/admin.py')

        return True

