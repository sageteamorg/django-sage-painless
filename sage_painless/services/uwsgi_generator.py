import os
import time

from django.conf import settings

from sage_painless import templates
from sage_painless.utils.jinja_service import JinjaHandler


class UwsgiGenerator(JinjaHandler):
    """generate uwsgi config"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def generate(self, chdir, home, module, master, pidfile, vacuum, max_requests, processes, daemonize):
        """generate uwsgi.ini"""
        start_time = time.time()

        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/uwsgi.ini',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'uwsgi.txt'),
            data={
                'chdir': chdir,
                'processes': processes if processes else 10,
                'home': home,
                'module': module,
                'master': master,
                'pidfile': pidfile,
                'vacuum': vacuum,
                'max_requests': max_requests if max_requests else 5000,
                'daemonize': daemonize if daemonize else '/var/log/uwsgi/uwsgi.log'
            }
        )

        end_time = time.time()
        return True, 'uwsgi config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
