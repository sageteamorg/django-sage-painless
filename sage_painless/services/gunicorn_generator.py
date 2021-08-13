import os
import time

from django.conf import settings

from sage_painless import templates
from sage_painless.utils.comment_service import CommentService
from sage_painless.utils.file_service import FileService
from sage_painless.utils.git_service import GitSupport
from sage_painless.utils.jinja_service import JinjaHandler
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.pep8_service import Pep8
from sage_painless.utils.timing_service import TimingService


class GunicornGenerator(
    JinjaHandler, JsonHandler, Pep8,
    FileService, CommentService, TimingService, GitSupport
):
    """gunicorn config generator"""
    DEPLOY_KEYWORD = 'deploy'
    GUNICORN_KEYWORD = 'gunicorn'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract_gunicorn_config(self, diagram):
        """extract gunicorn config from diagram json"""
        deploy = diagram.get(self.DEPLOY_KEYWORD)
        if not deploy:
            raise KeyError('`deploy` not set in diagram json file')
        return deploy.get(self.GUNICORN_KEYWORD)

    def generate(self, diagram_path, git_support=False):
        """generate conf.py
        template:
            sage_painless/templates/conf.txt
        """
        start_time = time.time()

        diagram = self.load_json(diagram_path)

        if git_support:
            self.init_repo(settings.BASE_DIR)

        config = self.extract_gunicorn_config(diagram)  # get gunicorn config from diagram

        # generate conf.py
        self.stream_to_template(
            output_path=f'{settings.BASE_DIR}/gunicorn-conf.py',
            template_path=os.path.abspath(templates.__file__).replace('__init__.py', 'conf.txt'),
            data={
                'config': config,
                'comments': self.GUNICORN_CONFIG_COMMENTS
            }
        )
        self.fix_pep8(f'{settings.BASE_DIR}/gunicorn-conf.py')
        if git_support:
            self.commit_file(
                f'{settings.BASE_DIR}/gunicorn-conf.py',
                f'deploy (gunicorn): Create gunicorn config file'
            )

        end_time = time.time()
        return True, 'gunicorn config generated ({:.3f} ms)'.format(self.calculate_execute_time(start_time, end_time))
