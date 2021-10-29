"""
django-sage-painless - README Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time
from platform import python_version

from django.conf import settings

# Base
from sage_painless.services.abstract import AbstractReadMeGenerator

# Helpers
from sage_painless.utils.file_service import FileService
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class ReadMeGenerator(AbstractReadMeGenerator, JinjaHandler, JsonHandler, Pep8, FileService, TimingService, GitSupport):
    """Generate README.md for project"""
    README_TEMPLATE = 'README.jinja'

    def __init__(self, *args, **kwargs):
        """init"""
        super().__init__(*args, **kwargs)

    def generate(self, diagram_path, git_support=False):
        """stream README.md to docs/sage_painless/git/README.md
        template:
            sage_painless/templates/README.jinja
        """
        start_time = time.time()
        diagram = self.load_json(diagram_path)

        # initialize
        self.create_dir_if_not_exists('docs')
        self.create_dir_if_not_exists('docs/sage_painless')
        self.create_dir_if_not_exists('docs/sage_painless/git')
        if git_support:
            self.init_repo(settings.BASE_DIR)

        modules = self.get_installed_module_names()
        django_apps = self.get_built_in_app_names()

        project_name = self.get_project_name()
        project_version = self.get_project_version()

        django_version = self.get_django_version()
        py_version = python_version()

        project_structure = self.make_tree(settings.BASE_DIR)

        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/docs/sage_painless/git/README.md',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.README_TEMPLATE),
            data={
                'project_name': project_name,
                'built_in_apps': django_apps,
                'installed_modules': modules,
                'django_version': django_version,
                'py_version': py_version,
                'project_version': project_version,
                'docker_support': self.has_docker_support(),
                'structure': project_structure
            }
        )
        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/docs/sage_painless/git/README.md',
                f'docs (git): Create README.md'
            )

        end_time = time.time()
        return True, 'README generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
