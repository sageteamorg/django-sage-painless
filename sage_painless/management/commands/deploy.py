import datetime

from django.core.management import BaseCommand

from sage_painless.services.docker_generator import DockerGenerator
from sage_painless.services.gunicorn_generator import GunicornGenerator
from sage_painless.services.tox_generator import ToxGenerator
from sage_painless.services.uwsgi_generator import UwsgiGenerator
from sage_painless.utils.report_service import ReportUserAnswer


class Command(BaseCommand):
    help = 'Generate all files need to deploy project.'

    def add_arguments(self, parser):
        """initialize arguments"""
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path that will generate from it')
        parser.add_argument('-g', '--git', type=bool, help='generate git commits')

    def handle(self, *args, **options):
        diagram_path = options.get('diagram')
        git_support = options.get('git', False)
        stdout_messages = list()  # initial empty messages

        reporter = ReportUserAnswer(
            app_name='deploy-config',
            file_prefix=f'deploy-config-{int(datetime.datetime.now().timestamp())}'
        )
        reporter.init_report_file()

        # generate gunicorn config
        gunicorn_support = input('Would you like to generate gunicorn config(yes/no)? ')
        gunicorn_support = True if gunicorn_support == 'yes' else False

        if gunicorn_support:
            reporter.add_question_answer(
                question='create gunicorn conf.py',
                answer=True
            )
            gunicorn_generator = GunicornGenerator()
            check, message = gunicorn_generator.generate(diagram_path, git_support=git_support)
            if check:
                stdout_messages.append(self.style.SUCCESS(f'deploy[INFO]: {message}'))
            else:
                stdout_messages.append(self.style.ERROR(f'deploy[ERROR]: {message}'))
        else:
            reporter.add_question_answer(
                question='create gunicorn conf.py',
                answer=False
            )

        # generate uwsgi config
        uwsgi_support = input('Would you like to generate uwsgi config(yes/no)? ')
        uwsgi_support = True if uwsgi_support == 'yes' else False

        if uwsgi_support:
            reporter.add_question_answer(
                question='create uwsgi.ini',
                answer=True
            )
            uwsgi_generator = UwsgiGenerator()
            check, message = uwsgi_generator.generate(diagram_path, git_support=git_support)
            if check:
                stdout_messages.append(self.style.SUCCESS(f'deploy[INFO]: {message}'))
            else:
                stdout_messages.append(self.style.ERROR(f'deploy[ERROR]: {message}'))
        else:
            reporter.add_question_answer(
                question='create uwsgi.ini',
                answer=False
            )

        # generate nginx config
        nginx_support = input('Would you like to generate nginx config(yes/no)? ')
        nginx_support = True if nginx_support == 'yes' else False

        # generate docker config
        docker_support = input('Would you like to dockerize your project(yes/no)? ')
        docker_support = True if docker_support == 'yes' else False

        if docker_support:
            reporter.add_question_answer(
                question='create docker-compose.yml',
                answer=True
            )
            reporter.add_question_answer(
                question='create Dockerfile',
                answer=True
            )

            docker_generator = DockerGenerator()
            check, message = docker_generator.generate(
                diagram_path,
                gunicorn_support=gunicorn_support,
                uwsgi_support=uwsgi_support,
                nginx_support=nginx_support,
                git_support=git_support
            )

            if check:
                stdout_messages.append(self.style.SUCCESS(f'deploy[INFO]: {message}'))
            else:
                stdout_messages.append(self.style.ERROR(f'deploy[ERROR]: {message}'))

        else:
            reporter.add_question_answer(
                question='create docker-compose.yml',
                answer=False
            )
            reporter.add_question_answer(
                question='create Dockerfile',
                answer=False
            )

        # generate tox config
        tox_support = input('Would you like to generate tox & coverage config files(yes/no)? ')
        tox_support = True if tox_support == 'yes' else False

        reporter = ReportUserAnswer(
            app_name='tox',
            file_prefix=f'tox-{int(datetime.datetime.now().timestamp())}'
        )
        reporter.init_report_file()

        if tox_support:
            reporter.add_question_answer(
                question='create tox & coverage config',
                answer=True
            )
            tox_generator = ToxGenerator()
            check, message = tox_generator.generate(diagram_path, git_support=git_support)
            if check:
                stdout_messages.append(self.style.SUCCESS(f'deploy[INFO]: {message}'))
            else:
                stdout_messages.append(self.style.ERROR(f'deploy[ERROR]: {message}'))
        else:
            reporter.add_question_answer(
                question='create tox & coverage config',
                answer=False
            )

        # print messages in terminal
        for message in stdout_messages:
            self.stdout.write(message)
