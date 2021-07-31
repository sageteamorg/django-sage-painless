import os
import time

from django.conf import settings

from sage_painless import templates
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler


class ToxGenerator(JinjaHandler, JsonHandler):
    """
    generate tox configs & coverage support
    """
    APPS_KEYWORD = 'apps'

    def __init__(self, *args, **kwargs):
        """init"""
        pass

    def get_app_names(self, diagram):
        """get diagram app names"""
        return diagram.get(self.APPS_KEYWORD).keys()

    def get_kernel_name(self):
        """get project kernel name"""
        return settings.SETTINGS_MODULE.split('.')[0]

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def generate(self, diagram_path):
        """generate files"""
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        app_names = self.get_app_names(diagram)
        kernel_name = self.get_kernel_name()
        # .coveragerc
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/.coveragerc',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'coveragerc.txt'),
            data={
                'app_names': app_names
            }
        )

        # tox.ini
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/tox.ini',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'tox.txt'),
            data={
                'kernel_name': kernel_name
            }
        )
        end_time = time.time()
        return True, 'Tox config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
