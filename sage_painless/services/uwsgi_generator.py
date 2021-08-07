import os
import time

from django.conf import settings

from sage_painless import templates
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.timing_service import TimingService


class UwsgiGenerator(JinjaHandler, JsonHandler, TimingService):
    """generate uwsgi config"""
    DEPLOY_KEYWORD = 'deploy'
    UWSGI_KEYWORD = 'uwsgi'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract_uwsgi_config(self, diagram):
        """extract uwsgi config from diagram json"""
        deploy = diagram.get(self.DEPLOY_KEYWORD)
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy.get(self.UWSGI_KEYWORD)

    def generate(self, diagram_path):
        """generate uwsgi.ini
        template:
            sage_painless/templates/uwsgi.txt
        """
        start_time = time.time()

        diagram = self.load_json(diagram_path)

        config = self.extract_uwsgi_config(diagram)  # get uwsgi config from diagram

        # generate uwsgi.ini
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/uwsgi.ini',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'uwsgi.txt'),
            data={
                'config': config
            }
        )

        end_time = time.time()
        return True, 'uwsgi config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
