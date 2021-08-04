import os
import time

from django.conf import settings

from sage_painless import templates
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.pep8_service import Pep8


class GunicornGenerator(JinjaHandler, Pep8):
    """gunicorn config generator"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def create_dir_if_not_exists(self, directory):
        if not os.path.exists(f'{settings.BASE_DIR}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{directory}')

    def generate(self, kernel_name, worker_class, worker_connections, access_log, error_log, workers):
        """generate conf.py"""
        start_time = time.time()

        # initialize
        self.create_dir_if_not_exists('config')
        self.create_dir_if_not_exists('config/gunicorn/')

        # generate conf.py
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/config/gunicorn/conf.py',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'conf.txt'),
            data={
                'kernel_name': kernel_name,
                'worker_class': worker_class if worker_class else 'gevent',
                'worker_connections': worker_connections if worker_connections else 3000,
                'access_log': access_log if access_log else '/var/log/gunicorn/gunicorn-access.log',
                'error_log': error_log if error_log else '/var/log/gunicorn/gunicorn-error.log',
                'workers': workers if workers else 5
            }
        )
        self.fix_pep8(f'{settings.BASE_DIR}/config/gunicorn/conf.py')

        end_time = time.time()
        return True, 'gunicorn config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
