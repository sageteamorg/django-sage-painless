import logging
import os
import subprocess

from django.conf import settings
from django.apps import apps
from django.db.models import ForeignKey, ManyToManyField, CharField, DateField, DateTimeField

from sqlalchemy.exc import ProgrammingError
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import drop_database, create_database
from sqlalchemy.sql import text

from jinja2 import Environment

from upload_center.model_classes.admin_model import AdminModel


class Generator:
    def __init__(
            self,
            diagram_path,
            base_dir,
            project_name,
            app_name,
            create_model,
            create_admin,
            create_api,
            create_doc
    ):
        self.diagram_path = diagram_path
        self.base_name = base_dir
        self.base_dir = settings.BASE_DIR + f'/{settings.PROJECTS_DIR}/' + base_dir
        self.project_name = project_name
        self.app_name = app_name
        self.create_model = create_model
        self.create_admin = create_admin
        self.create_api = create_api
        self.create_doc = create_doc

    # def load_jinja_template(self, template_path):
    #     """
    #     load jinja template from template_path
    #     """
    #     env = Environment(autoescape=False, optimized=False)
    #     with open(template_path, 'r') as t:
    #         template = env.from_string(t.read())
    #     return template
    #
    # def stream_data_to_jinja(self, template_path, data_dict: dict, output_path):
    #     """
    #     stream data to jinja template
    #     """
    #     template = self.load_jinja_template(template_path)
    #     with open(output_path, 'w') as o:
    #         template.stream(
    #             **data_dict
    #         ).dump(o)
    #     return True

    def generate_admin(self):
        """
        generate admin.py from created models.py
        """
        pass
        # admin_models = list()
        #
        # # prepare data for jinja template
        # model_classes = self.get_app_models(self.app_name)
        # for model in model_classes:
        #     admin_model = AdminModel()
        #     admin_model.set_model_name(model._meta.lable.split('.')[1])
        #     admin_model.set_model(model)
        #     admin_model.set_fields(self.get_model_fields(model))
        #     admin_model.set_char_fields(self.get_char_fields(model))
        #     admin_model.set_fk_fields(self.get_foreign_key_fields(model))
        #     admin_model.set_m2m_fields(self.get_many_to_many_fields(model))
        #     admin_models.append(admin_model)
        #
        # # create admin.py from jinja template
        # self.stream_data_to_jinja(
        #     template_path='templates/admin_template.txt',
        #     data_dict={
        #         'app_name': self.app_name,
        #         'models': admin_models
        #     },
        #     output_path=f'{self.base_dir}/{self.app_name}/admin.py'
        # )

    # def get_app_models(self, app_label):
    #     """
    #     get list of app models
    #     """
    #     from importlib import import_module
    #     os.chdir(self.base_dir)
    #     apps_ = import_module(f'{self.app_name}.apps')
    #     app_config = [obj for obj in dir(apps_)][0]
    #     app_config = eval(f'{self.app_name}.apps.{app_config}')
    #     app_models = app_config.get_models()
    #     return app_models

    # def get_model_fields(self, model_class):
    #     """
    #     get all fields of a model
    #     """
    #     return model_class._meta.get_fields()
    #
    # def get_foreign_key_fields(self, model_class):
    #     """
    #     get foreign key fields of a model
    #     """
    #     fields = self.get_model_fields(model_class)
    #     fk_fields = [field for field in fields if type(field) == ForeignKey]
    #     return fk_fields
    #
    # def get_many_to_many_fields(self, model_class):
    #     """
    #     get many to many fields of a model
    #     """
    #     fields = self.get_model_fields(model_class)
    #     m2m_fields = [field for field in fields if type(field) == ManyToManyField]
    #     return m2m_fields
    #
    # def get_char_fields(self, model_class):
    #     """
    #     get char field fields of a model
    #     """
    #     fields = self.get_model_fields(model_class)
    #     char_fields = [field for field in fields if type(field) == CharField]
    #     return char_fields
    #
    # def get_datetime_fields(self, model_class):
    #     """
    #     get date/datetime fields of a model
    #     """
    #     fields = self.get_model_fields(model_class)
    #     datetime_fields = [
    #         field for field in fields if type(field) == DateField or type(field) == DateTimeField
    #     ]
    #     return datetime_fields

    def create_project(self):
        """
        create django project
        """
        os.chdir(settings.BASE_DIR)
        if not os.path.exists(settings.PROJECTS_DIR):
            os.mkdir(settings.PROJECTS_DIR)
        os.chdir(settings.PROJECTS_DIR)
        os.mkdir(self.base_name)
        os.chdir(self.base_dir)
        subprocess.run(
            [
                'django-admin',
                'startproject',
                self.project_name,
                '.'
            ]
        )
        return True

    def create_app(self):
        """
        create django app
        add app to settings.py
        """
        if os.path.exists(f'{self.base_dir}/{self.app_name}'):
            return True
        os.chdir(self.base_dir)
        subprocess.run(
            [
                'python',
                'manage.py',
                'startapp',
                self.app_name
            ]
        )

        with open(f'{self.base_dir}/{self.project_name}/settings.py', 'a+') as f:
            f.writelines([f'\nINSTALLED_APPS.append("{self.app_name}")'])
            f.close()
        return True

    def migrate_project(self):
        """
        migrate django project
        """
        os.chdir(self.base_dir)
        subprocess.run(
            [
                'python',
                'manage.py',
                'makemigrations'
            ]
        )
        subprocess.run(
            [
                'python',
                'manage.py',
                'migrate'
            ]
        )
        return True

    def generate(self):
        # pre process
        check = self.create_project()
        if check:
            logging.info(
                'project {} created successfully'.format(self.project_name)
            )
            check = self.create_app()
            if check:
                logging.info(
                    'app {} created successfully'.format(self.app_name)
                )
                # create models
                if self.create_model:
                    self.generate_models()
                    logging.info(
                        'models.py generated successfully in app {}'.format(self.app_name)
                    )
                if self.create_admin:
                    self.generate_admin()
                    logging.info(
                        'admin.py generated successfully in app {}'.format(self.app_name)
                    )
            else:
                raise IOError('Error in creating App')
        else:
            raise IOError('Error in creating Project')
