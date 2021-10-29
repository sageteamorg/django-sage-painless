"""
django-sage-painless - UWSGI Config Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractUWSGIGenerator

# Helpers
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class UwsgiGenerator(AbstractUWSGIGenerator, JinjaHandler, JsonHandler, TimingService, GitSupport):
    """generate uwsgi config"""
    UWSGI_TEMPLATE = 'uwsgi.jinja'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path, git_support=False):
        """generate uwsgi.ini
        template:
            sage_painless/templates/uwsgi.jinja
        """
        start_time = time.time()

        diagram = self.load_json(diagram_path)

        config = self.extract_uwsgi_config(diagram)  # get uwsgi config from diagram

        if git_support:
            self.init_repo(settings.BASE_DIR)

        # generate uwsgi.ini
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/uwsgi.ini',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.UWSGI_TEMPLATE),
            data={
                'config': config
            }
        )

        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/uwsgi.ini',
                f'deploy (uwsgi): Create uwsgi config file'
            )

        end_time = time.time()
        return True, 'uwsgi config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
