import datetime

from django.core.management import BaseCommand

from sage_painless.services.docker_generator import DockerGenerator
from sage_painless.services.gunicorn_generator import GunicornGenerator
from sage_painless.services.tox_generator import ToxGenerator
from sage_painless.utils.report_service import ReportUserAnswer


class Command(BaseCommand):
    help = 'Generate all files need to deploy project.'

    def add_arguments(self, parser):
        """initialize arguments"""
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path that will generate from it')

    def handle(self, *args, **options):
        diagram_path = options.get('diagram')
        stdout_messages = list()  # initial empty messages

        # generate docker config
        docker_support = input('Would you like to dockerize your project(yes/no)? ')

        reporter = ReportUserAnswer(
            app_name='deploy-config',
            file_prefix=f'deploy-config-{int(datetime.datetime.now().timestamp())}'
        )
        reporter.init_report_file()

        if docker_support == 'yes':
            reporter.add_question_answer(
                question='create docker-compose.yml',
                answer=True
            )
            reporter.add_question_answer(
                question='create Dockerfile',
                answer=True
            )
            db_image = input("Please enter your project's database image(e.g postgres): ")
            db_name = input('Please enter database name: ')
            db_user = input('Please enter database user username: ')
            db_pass = input('Please enter database user password: ')
            redis_support = input('Would you like to config redis server for your project(yes/no)? ')
            rabbit_support = input('Would you like to config rabbitMQ for your project(yes/no)? ')
            rabbit_user = None
            rabbit_pass = None
            if rabbit_support == 'yes':
                reporter.add_question_answer(
                    question='rabbitmq support',
                    answer=True
                )
                rabbit_user = input('Please enter rabbitMQ user username: ')
                rabbit_pass = input('Please enter rabbitMQ user password: ')
            else:
                reporter.add_question_answer(
                    question='rabbitmq support',
                    answer=False
                )

            if redis_support == 'yes':
                reporter.add_question_answer(
                    question='redis support',
                    answer=True
                )
            else:
                reporter.add_question_answer(
                    question='redis support',
                    answer=False
                )

            redis_support = True if redis_support == 'yes' else False
            rabbit_support = True if rabbit_support == 'yes' else False

            docker_generator = DockerGenerator(
                db_image, db_name, db_user, db_pass,
                redis_support, rabbit_support,
                rabbit_user, rabbit_pass
            )

            check, message = docker_generator.generate()

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

        # generate gunicorn config
        gunicorn_support = input('Would you like to generate gunicorn config(yes/no)? ')

        if gunicorn_support == 'yes':
            reporter.add_question_answer(
                question='create gunicorn conf.py',
                answer=True
            )
            kernel_name = input("Please enter your django project's root name(e.g kernel): ")
            worker_class = input('Please enter gunicorn worker class(default: gevent): ')
            worker_connections = input('Please enter gunicorn worker connections count(default: 3000): ')
            workers = input('Please enter gunicorn workers count(default: 5): ')
            access_log = input(
                'Please enter gunicorn access log path(default: /var/log/gunicorn/gunicorn-access.log): ')
            error_log = input(
                'Please enter gunicorn error log path(default: /var/log/gunicorn/gunicorn-error.log): ')

            gunicorn_generator = GunicornGenerator()
            check, message = gunicorn_generator.generate(
                kernel_name,
                worker_class,
                worker_connections,
                access_log,
                error_log,
                workers
            )
            if check:
                stdout_messages.append(self.style.SUCCESS(f'deploy[INFO]: {message}'))
            else:
                stdout_messages.append(self.style.ERROR(f'deploy[ERROR]: {message}'))
        else:
            reporter.add_question_answer(
                question='create gunicorn conf.py',
                answer=False
            )

        # generate tox config
        tox_support = input('Would you like to generate tox & coverage config files(yes/no)? ')

        reporter = ReportUserAnswer(
            app_name='tox',
            file_prefix=f'tox-{int(datetime.datetime.now().timestamp())}'
        )
        reporter.init_report_file()

        if tox_support == 'yes':
            reporter.add_question_answer(
                question='create tox & coverage config',
                answer=True
            )
            tox_generator = ToxGenerator()
            version = input('Please enter the version of your project: ')
            description = input('Please enter a description for your project: ')
            author = input('Please enter author name/names: ')
            req_path = input('Please enter the path of your requirements.txt (default: requirements.txt): ')
            req_path = req_path if req_path else 'requirements.txt'
            check, message = tox_generator.generate(
                diagram_path=diagram_path,
                version=version,
                description=description,
                author=author,
                req_path=req_path
            )
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
