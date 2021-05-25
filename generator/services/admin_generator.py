from django.apps import apps
from django.conf import settings
from generator.services.jinja_service import stream_to_template


class AdminGenerator:
    def __init__(self, app_label):
        self.app_label = app_label

    def generate(self):
        """
        generate admin.py for given app
        """
        models = list(apps.get_app_config('api').get_models())
        models = [model.__name__ for model in models]
        stream_to_template(
            output_path=f'{settings.BASE_DIR}/{self.app_label}/admin.py',
            template_path=f'{settings.BASE_DIR}/generator/templates/admin.txt',  # TODO: Should be dynamic
            data={
                'app_name': self.app_label,
                'models': models,
            }
        )

        return True

