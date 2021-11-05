"""
django-sage-painless - Gunicorn Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractGunicornGenerator

# Helpers
from sage_painless.utils.comment_service import CommentService
from sage_painless.utils.file_service import FileService
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class GunicornGenerator(
    AbstractGunicornGenerator, JinjaHandler, JsonHandler, Pep8, FileService, CommentService, TimingService, GitSupport
):
    """gunicorn config generator"""
    CONF_TEMPLATE = 'conf.jinja'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path, git_support=False):
        """generate conf.py
        template:
            sage_painless/templates/conf.jinja
        """
        start_time = time.time()

        diagram = self.load_json(diagram_path)

        if git_support:
            self.init_repo(settings.BASE_DIR)

        config = self.extract_gunicorn_config(diagram)  # get gunicorn config from diagram

        # generate conf.py
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/gunicorn-conf.py',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.CONF_TEMPLATE),
            data={
                'config': config,
                'comments': self.GUNICORN_CONFIG_COMMENTS
            }
        )
        self.fix_pep8(f'{settings.BASE_DIR}/gunicorn-conf.py')
        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/gunicorn-conf.py',
                f'deploy (gunicorn): Create gunicorn config file'
            )

        end_time = time.time()
        return True, 'gunicorn config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
