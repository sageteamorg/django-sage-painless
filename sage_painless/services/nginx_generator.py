"""
django-sage-painless - Nginx Config Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractNiginxGenerator

# Helpers
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class NginxGenerator(
    AbstractNiginxGenerator, JinjaHandler, TimingService, GitSupport
):
    NGINX_TEMPLATE = 'nginx.jinja'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self, git_support=False):
        """generate nginx.conf
        template:
            sage_painless/templates/nginx.jinja
        """
        start_time = time.time()

        if git_support:
            self.init_repo(settings.BASE_DIR)

        # generate nginx.conf
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/nginx.conf',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.NGINX_TEMPLATE),
            data={
                'static_files': self.get_static_files_dir(),
                'media_files': self.get_media_files_dir()
            }
        )

        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/nginx.conf',
                f'deploy (nginx): Create nginx config file'
            )

        end_time = time.time()
        return True, 'nginx config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
