"""
django-sage-painless - Generator Constants Observer Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
from abc import ABC


class GeneratorConstants(ABC):
    """Generator Constant Variables"""
    MODELS_KEYWORD = 'models'
    APPS_KEYWORD = 'apps'
    FIELDS_KEYWORD = 'fields'
    TYPE_KEYWORD = 'type'
    ENCRYPTED_KEYWORD = 'encrypt'
    STREAM_KEYWORD = 'stream'
    VALIDATORS_KEYWORD = 'validators'
    FUNC_KEYWORD = 'func'
    ARG_KEYWORD = 'arg'
    ADMIN_KEYWORD = 'admin'
    API_KEYWORD = 'api'
    API_DIR = 'api'
    TESTS_DIR = 'tests'
    DEPLOY_KEYWORD = 'deploy'
    DOCKER_KEYWORD = 'docker'
    GUNICORN_KEYWORD = 'gunicorn'
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
    TOX_KEYWORD = 'tox'
    UWSGI_KEYWORD = 'uwsgi'
    PERMISSION_KEYWORD = 'permission'
    METHODS_KEYWORD = 'methods'
    FILTER_KEYWORD = 'filter'
    SEARCH_KEYWORD = 'search'

    def get_constant(self, name):
        """get constant from variables"""
        if hasattr(self, name):
            return getattr(self, name)
        raise NameError(f'name {name} is not defined')

    def set_constant(self, name, value):
        """set constant variable in subclass"""
        return setattr(self, name, value)
