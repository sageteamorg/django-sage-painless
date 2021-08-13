import os
import time

from django.conf import settings
from django.core.management.utils import get_random_secret_key

from sage_painless import templates
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.timing_service import TimingService


class DockerGenerator(JinjaHandler, JsonHandler, TimingService, GitSupport):
    """Generate DockerFile & docker-compose"""
    DEPLOY_KEYWORD = 'deploy'
    DOCKER_KEYWORD = 'docker'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_kernel_name(self):
        """get project kernel name"""
        return settings.SETTINGS_MODULE.split('.')[0]

    def extract_deploy_config(self, diagram):
        """extract deploy deploy config from diagram"""
        deploy = diagram.get(self.DEPLOY_KEYWORD)
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy

    def get_staticfiles_dir(self):
        """get staticfiles dir
        `web` is container name
        """
        directory = settings.STATIC_ROOT
        if not directory:
            raise SystemError('STATIC_ROOT should be set in your settings')
        return directory.replace(self.get_kernel_name(), 'web')

    def get_mediafiles_dir(self):
        """get mediafiles dir
        `web` is container name
        """
        directory = settings.MEDIA_ROOT
        if not directory:
            raise SystemError('MEDIA_ROOT should be set in your settings')
        return directory.replace(self.get_kernel_name(), 'web')

    def generate(self, diagram_path, gunicorn_support=False, uwsgi_support=False, nginx_support=False, git_support=False):
        """stream docker configs to root
        template:
            sage_painless/templates/Dockerfile.txt
            sage_painless/templates/docker-compose.txt
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
            }
        }
        config = self.extract_deploy_config(diagram)  # get deploy config from diagram
        default_config.update(config)  # update default config with user input

        # stream to Dockerfile
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/Dockerfile',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'Dockerfile.txt'),
            data={
                'nginx': nginx_support,
                'kernel_name': self.get_kernel_name()
            }
        )

        # stream to docker-compose.yml
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/docker-compose.yml',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'docker-compose.txt'),
            data={
                'kernel': self.get_kernel_name(),
                'docker_config': default_config.get('docker'),
                'gunicorn_config': default_config.get('gunicorn'),
                'uwsgi_config': default_config.get('uwsgi'),
                'gunicorn': gunicorn_support,
                'uwsgi': uwsgi_support,
                'nginx': nginx_support
            }
        )

        # stream to .env.prod
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/.env.prod',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'env.txt'),
            data={
                'config': default_config.get('docker'),
                'random_secret_key': get_random_secret_key(),
                'debug': 1 if settings.DEBUG else 0,
                'allowed_hosts': settings.ALLOWED_HOSTS
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

        # stream to nginx.conf
        if nginx_support:
            self.stream_to_template(
                output_path=f'{settings.BASE_DIR}/nginx.conf',
                template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'nginx.txt'),
                data={
                    'kernel_name': self.get_kernel_name(),
                    'staticfiles': self.get_staticfiles_dir(),
                    'mediafiles': self.get_mediafiles_dir()
                }
            )
            if git_support:
                self.commit_file(
                    f'{settings.BASE_DIR}/nginx.conf',
                    f'deploy (nginx): Create nginx.conf'
                )

        end_time = time.time()
        return True, 'Docker config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
