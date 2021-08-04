import os
import time
from pathlib import Path
from platform import python_version

import django
from django.apps import apps
from django.conf import settings

from sage_painless import templates
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8


class ReadMeGenerator(JinjaHandler, JsonHandler, Pep8):
    """Generate README.md for project"""

    APPS_KEYWORD = 'apps'
    SPACE = '    '
    BRANCH = '│   '
    TEE = '├── '
    LAST = '└── '
    IGNORE_DIRS = [
        'venv', '.pytest_cache',
        '.tox', '.vscode', 'dist',
        '.git', '__pycache__', '_build',
        '_static', '_templates',
    ]

    def __init__(self):
        """init"""
        pass

    def get_built_in_app_names(self):
        """django built-in apps"""
        return [app.verbose_name for app in apps.get_app_configs() if app.name.startswith('django.')]

    def get_installed_module_names(self):
        """extra installed modules to setting"""
        return [app.verbose_name for app in apps.get_app_configs() if not app.name.startswith('django.')]

    def get_project_name(self):
        """get project root name"""
        base_dir = settings.BASE_DIR
        return base_dir.name if hasattr(base_dir, 'name') else base_dir

    def get_project_version(self):
        """get current project version if set"""
        return getattr(settings, 'VERSION', '1.0.0')

    def get_django_version(self):
        """get current Django version"""
        return django.get_version()

    def merge(self, list_a: list, list_b: list):
        """merge 2 lists"""
        return list(set(list_a + list_b))

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def create_dir_if_not_exists(self, directory):
        if not os.path.exists(f'{settings.BASE_DIR}/{directory}'):
            os.mkdir(f'{settings.BASE_DIR}/{directory}')

    def has_docker_support(self):
        """is project dockerized"""
        compose_file_yml = Path(f'{settings.BASE_DIR}/docker-compose.yml')
        compose_file_yaml = Path(f'{settings.BASE_DIR}/docker-compose.yaml')

        if compose_file_yml.is_file() or compose_file_yaml.is_file():
            return True

        return False

    def make_tree(self, dir_path: Path, prefix: str = ''):
        """create project root tree structure"""
        contents = list(dir_path.iterdir())
        pointers = [self.TEE] * (len(contents) - 1) + [self.LAST]

        for pointer, path in zip(pointers, contents):
            if path.name not in self.IGNORE_DIRS:
                yield prefix + pointer + path.name
                if path.is_dir():
                    extension = self.BRANCH if pointer == self.TEE else self.SPACE
                    yield from self.make_tree(path, prefix=prefix + extension)

    def generate(self, diagram_path):
        """stream README.md to docs/sage_painless/git/README.md"""
        start_time = time.time()
        diagram = self.load_json(diagram_path)

        # initialize
        self.create_dir_if_not_exists('docs')
        self.create_dir_if_not_exists('docs/sage_painless')
        self.create_dir_if_not_exists('docs/sage_painless/git')

        modules = self.get_installed_module_names()
        django_apps = self.get_built_in_app_names()

        project_name = self.get_project_name()
        project_version = self.get_project_version()

        django_version = self.get_django_version()
        py_version = python_version()

        project_structure = self.make_tree(settings.BASE_DIR)

        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/docs/sage_painless/git/README.md',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'README.txt'),
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

        end_time = time.time()
        return True, 'README generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
