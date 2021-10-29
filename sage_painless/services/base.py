"""
django-sage-painless - Base Generator Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """Generator Abstract"""

    @abstractmethod
    def generate(self, *args, **kwargs):
        """generate process
        serialize data & push to jinja2 template
        """
        raise NotImplementedError('Should implement in subclass')

    def set_template(self, template_key, template_file):
        """set template
        template file should be in sage_painless/templates folder
        """
        setattr(self, f'template_{template_key}', template_file)

    def get_template(self, template_key):
        if hasattr(self, f'template_{template_key}'):
            return getattr(self, f'template_{template_key}')
        raise NameError(f'template key {template_key} is not defined')

    def register_method(self, name):
        """register a method in class
        registered method should implement in subclass
        e.g:
        normalize_models(self, diagram):
            return diagram.keys()
        """
        def _method(self, *args, **kwargs):
            raise NotImplementedError('Registered method should implement in subclass')
        setattr(BaseGenerator, name, _method)
