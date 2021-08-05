import os
import time

from django.conf import settings

from sage_painless import templates
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler


class DockerGenerator(JinjaHandler, JsonHandler):
    """Generate DockerFile & docker-compose"""
    DEPLOY_KEYWORD = 'deploy'
    DOCKER_KEYWORD = 'docker'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0

    def extract_docker_config(self, diagram):
        """extract docker deploy config from diagram"""
        deploy = diagram.get(self.DEPLOY_KEYWORD)
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy.get(self.DOCKER_KEYWORD)

    def generate(self, diagram_path):
        """stream docker configs to root
        template:
            sage_painless/templates/Dockerfile.txt
            sage_painless/templates/docker-compose.txt
        """
        start_time = time.time()

        diagram = self.load_json(diagram_path)

        config = self.extract_docker_config(diagram)  # get docker config from diagram

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
                'config': config
            }
        )
        end_time = time.time()
        return True, 'Docker config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
