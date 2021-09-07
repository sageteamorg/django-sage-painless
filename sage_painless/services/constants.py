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

    def get_constant(self, name):
        """get constant from variables"""
        if hasattr(self, name):
            return getattr(self, name)
        raise NameError(f'name {name} is not defined')

    def set_constant(self, name, value):
        """set constant variable in subclass"""
        return setattr(self, name, value)
