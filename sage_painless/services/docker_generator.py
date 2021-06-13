import os

from django.conf import settings

from sage_painless.utils.jinja_service import JinjaHandler

from sage_painless import templates


class DockerGenerator(JinjaHandler):
    """
    Generate DockerFile & docker-compose
    """

    def __init__(
            self,
            app_label,
            version,
            db_image,
            db_name,
            db_user,
            db_pass,
            redis_support,
            rabbit_support,
            rabbitmq_user=None,
            rabbitmq_pass=None
    ):
        self.redis = redis_support
        self.rabbtmq = rabbit_support
        self.rabbtmq_user = rabbitmq_user
        self.rabbtmq_pass = rabbitmq_pass
        self.db_image = db_image
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.app_name = app_label
        self.version = version

    def generate(self):
        """
        stream docker configs to root
        """

        # stream to Dockerfile
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/Dockerfile',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'Dockerfile.txt'),
        )

        # stream to docker-compose.yml
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/docker-compose.yml',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'docker-compose.txt'),
            data={
                'version': self.version,
                'db_image': self.db_image,
                'db_name': self.db_name,
                'db_user': self.db_user,
                'db_pass': self.db_pass,
                'redis_support': self.redis,
                'rabbit_support': self.rabbtmq,
                'rabbitmq_user': self.rabbtmq_user,
                'rabbitmq_pass': self.rabbtmq_pass
            }
        )

        return True, 'Docker config Generated Successfully. Changes are in these files:\nDockerfile\ndocker-compose.yml\n'
