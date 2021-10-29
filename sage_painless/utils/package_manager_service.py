"""
django-sage-painless - Package Manager Integration Main Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import subprocess

from django.conf import settings


class PackageManagerSupport:
    VALID_MANAGERS = ['pip', 'pipenv', 'Pipenv', 'poetry']
    COMMANDS = {
        'pip': ['pip freeze > requirements.txt'],
        'pipenv': ['pipenv lock -r > requirements.txt'],
        'Pipenv': ['pipenv lock -r > requirements.txt'],
        'poetry': ['poetry export -f requirements.txt --output requirements.txt']
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = None

    def validate_package_manager_type(self, _type):
        """check manager type is valid"""
        if _type not in self.VALID_MANAGERS:
            raise KeyError(f'package manager {_type} is not supported')

    def check_manager_is_ready(self):
        """check self.manager is set"""
        if not self.manager:
            raise NotImplementedError('self.manager should set first')

    def set_package_manager_type(self, _type):
        """set self.manager"""
        self.validate_package_manager_type(_type)
        self.manager = _type
        return self.manager

    @classmethod
    def run_requirements_command(cls, manager):
        """get export req command for each package manager
        call using subprocess
        """
        command = cls.COMMANDS.get(manager)
        if command:
            os.chdir(settings.BASE_DIR)  # go to base dir
            subprocess.call(command, shell=True)  # export packages
        else:
            SystemError('command not found for exporting requirements')

    def export_requirements(self):
        """export requirement packages"""
        self.check_manager_is_ready()
        self.run_requirements_command(self.manager)
