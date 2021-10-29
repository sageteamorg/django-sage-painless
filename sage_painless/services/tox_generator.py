"""
django-sage-painless - Tox Config Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractToxGenerator

# Helpers
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class ToxGenerator(AbstractToxGenerator, JinjaHandler, JsonHandler, Pep8, TimingService, GitSupport):
    """generate tox configs & coverage support"""
    COVERAGERC_TEMPLATE = 'coveragerc.jinja'
    TOX_TEMPLATE = 'tox.jinja'
    SETUP_TEMPLATE = 'setup.jinja'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path, git_support=False):
        """generate tox and coverage config
        template:
            sage_painless/templates/tox.jinja
            sage_painless/templates/coveragerc.jinja
            sage_painless/templates/setup.jinja
        """
        start_time = time.time()
        diagram = self.load_json(diagram_path)
        app_names = self.get_app_names()
        kernel_name = self.get_kernel_name()

        config = self.extract_tox_config(diagram)

        if git_support:
            self.init_repo(settings.BASE_DIR)

        # .coveragerc
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/.coveragerc',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.COVERAGERC_TEMPLATE),
            data={
                'app_names': app_names
            }
        )

        # tox.ini
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/tox.ini',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.TOX_TEMPLATE),
            data={
                'kernel_name': kernel_name
            }
        )

        # setup.py
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/setup.py',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.SETUP_TEMPLATE),
            data={
                'kernel_name': kernel_name,
                'config': config,
                'reqs': self.parse_requirements(config.get('req_path'))
            }
        )
        self.fix_pep8(f'{settings.BASE_DIR}/setup.py')

        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/.coveragerc',
                f'docs (coverage): Add coverage config file'
            )
            self.commit_file(
                f'{settings.BASE_DIR}/tox.ini',
                f'docs (tox): Add tox config file'
            )
            self.commit_file(
                f'{settings.BASE_DIR}/setup.py',
                f'docs (python): Create setup file'
            )

        end_time = time.time()
        return True, 'Tox config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
