import os
import time

from django.conf import settings
from django.apps import apps

from sage_painless import templates
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService


class ToxGenerator(JinjaHandler, JsonHandler, Pep8, TimingService, GitSupport):
    """generate tox configs & coverage support"""
    APPS_KEYWORD = 'apps'
    DEPLOY_KEYWORD = 'deploy'
    TOX_KEYWORD = 'tox'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_app_names(self):
        """get diagram app names"""
        return [app.name for app in apps.get_app_configs() if not app.name.startswith('django.')]

    def get_kernel_name(self):
        """get project kernel name"""
        return settings.SETTINGS_MODULE.split('.')[0]

    def parse_requirements(self, requirements):
        with open(requirements) as f:
            return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

    def extract_tox_config(self, diagram):
        """extract tox config from diagram json"""
        deploy = diagram.get(self.DEPLOY_KEYWORD)
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy.get(self.TOX_KEYWORD)

    def generate(self, diagram_path, git_support=False):
        """generate tox and coverage config
        template:
            sage_painless/templates/tox.txt
            sage_painless/templates/coveragerc.txt
            sage_painless/templates/setup.txt
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

        # setup.py
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/setup.py',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'setup.txt'),
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
