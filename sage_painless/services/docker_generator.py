"""
django-sage-painless - Docker Generator

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""
import os
import time

from django.conf import settings
from django.core.management.utils import get_random_secret_key

# Base
from sage_painless.services.abstract import AbstractDockerGenerator

# Helpers
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.package_manager_service import PackageManagerSupport
from sage_painless.utils.timing_service import TimingService

from sage_painless import templates


class DockerGenerator(AbstractDockerGenerator, JinjaHandler, JsonHandler, TimingService, GitSupport, PackageManagerSupport):
    """Generate DockerFile & docker-compose"""
    DOCKERFILE_TEMPLATE = 'Dockerfile.jinja'
    DOCKER_COMPOSE_TEMPLATE = 'docker-compose.jinja'
    ENV_TEMPLATE = 'env.jinja'
    NGINX_TEMPLATE = 'nginx.jinja'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(
            self, diagram_path, gunicorn_support=False, uwsgi_support=False,
            nginx_support=False, git_support=False, package_manager_support=False
    ):
        """stream docker configs to root
        template:
            sage_painless/templates/Dockerfile.jinja
            sage_painless/templates/docker-compose.jinja
        """
        start_time = time.time()

        diagram = self.load_json(diagram_path)
        if git_support:
            self.init_repo(settings.BASE_DIR)

        default_config = {
            "docker": {
                "db_image": "postgres",
                "db_name": "products",
                "db_user": "postgres",
                "db_pass": "postgres1234",
                "redis": False,
                "rabbitmq": False
            },
            "gunicorn": {
                "reload": False
            },
            "uwsgi": {
                "chdir": "/src/kernel",
                "home": "/src/venv",
                "module": "kernel.wsgi",
                "master": True,
                "pidfile": "/tmp/project-master.pid",
                "vacuum": False,
                "max-requests": 3000,
                "processes": 10,
                "daemonize": "/var/log/uwsgi/uwsgi.log"
            },
            "package_manager": {
                "type": "pip"
            }
        }
        config = self.extract_deploy_config(diagram)  # get deploy config from diagram
        default_config.update(config)  # update default config with user input

        # package manager
        if package_manager_support:
            manager = default_config.get('package_manager').get('type')
            self.set_package_manager_type(manager)
            self.export_requirements()

        # stream to Dockerfile
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/Dockerfile',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.DOCKERFILE_TEMPLATE),
            data={
                'gunicorn': gunicorn_support,
                'kernel_name': self.get_kernel_name()
            }
        )

        # stream to docker-compose.yml
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/docker-compose.yml',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.DOCKER_COMPOSE_TEMPLATE),
            data={
                'kernel': self.get_kernel_name(),
                'docker_config': default_config.get('docker', {}),
                'gunicorn': gunicorn_support
            }
        )

        # stream to .env.prod
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/.env.prod',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', self.ENV_TEMPLATE),
            data={
                'config': default_config.get('docker', {}),
                'random_postgres_password': get_random_secret_key(),
                'random_rabbitmq_password': get_random_secret_key()
            }
        )
        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/Dockerfile',
                f'deploy (docker): Create Dockerfile'
            )
            self.commit_file(
                f'{settings.BASE_DIR}/docker-compose.yml',
                f'deploy (docker): Create docker-compose.yml'
            )
            self.commit_file(
                f'{settings.BASE_DIR}/.env.prod',
                f'deploy (docker): Add variables to .env'
            )

        end_time = time.time()
        return True, 'Docker config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
