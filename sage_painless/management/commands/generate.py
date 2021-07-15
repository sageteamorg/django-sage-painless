import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from sage_painless.services.model_generator import ModelGenerator
from sage_painless.services.admin_generator import AdminGenerator
from sage_painless.services.api_generator import APIGenerator
from sage_painless.services.test_generator import TestGenerator
from sage_painless.services.docker_generator import DockerGenerator
from sage_painless.utils.report_service import ReportUserAnswer


class Command(BaseCommand):
    help = 'Generate all files need to your new app.'

    def add_arguments(self, parser):
        """initialize arguments"""
        parser.add_argument('-a', '--app', type=str, help='app label that will generate models.py for')
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path that will make models.py from it')

    def validate_settings(self, step):
        """validate required settings in each step"""
        if not 'sage_painless' in settings.INSTALLED_APPS:
            raise IOError('Add `sage_painless` to your INSTALLED_APPS')

        if step == 'api':
            if not 'rest_framework' in settings.INSTALLED_APPS:
                raise IOError('Add `rest_framework` to your INSTALLED_APPS')

        if step == 'test':
            if not 'rest_framework' in settings.INSTALLED_APPS:
                raise IOError('Add `rest_framework` to your INSTALLED_APPS')
            if not 'django_seed' in settings.INSTALLED_APPS:
                raise IOError('Add `django_seed` to your INSTALLED_APPS')

        if step == 'docs':
            if not 'drf_yasg' in settings.INSTALLED_APPS:
                raise IOError('Add `drf_yasg` to your INSTALLED_APPS')

    def handle(self, *args, **options):
        """get configs from user and generate"""
        app_label = options.get('app').replace('/', '')
        diagram_path = options.get('diagram')
        create_model = input('Would you like to generate models.py(yes/no)? ')
        create_admin = input('Would you like to generate admin.py(yes/no)? ')
        create_api = input('Would you like to generate serializers.py & views.py(yes/no)? ')
        create_test = input('Would you like to generate test for your project(yes/no)? ')
        cache_support = input('Would you like to add cache queryset support(yes/no)? ')
        docker_support = input('Would you like to dockerize your project(yes/no)? ')

        reporter = ReportUserAnswer(
            app_name=app_label,
            file_prefix=f'{app_label}-{datetime.date.today()}'
        )
        reporter.init_report_file()

        stdout_messages = list()

        if create_model == 'yes':
            model_generator = ModelGenerator(app_label)
            reporter.add_question_answer(
                question='create models.py',
                answer=True
            )
            if cache_support == 'yes':
                reporter.add_question_answer(
                    question='cache support',
                    answer=True
                )
                check, message = model_generator.generate_models(diagram_path, True)
            else:
                reporter.add_question_answer(
                    question='cache support',
                    answer=False
                )
                check, message = model_generator.generate_models(diagram_path)

            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))
        else:
            reporter.add_question_answer(
                question='create models.py',
                answer=False
            )

        if create_admin == 'yes':
            reporter.add_question_answer(
                question='create admin.py',
                answer=True
            )
            admin_generator = AdminGenerator(app_label)
            check, message = admin_generator.generate(diagram_path)
            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))
        else:
            reporter.add_question_answer(
                question='create admin.py',
                answer=False
            )

        if create_api == 'yes':
            reporter.add_question_answer(
                question='create serializers.py',
                answer=True
            )
            reporter.add_question_answer(
                question='create views.py',
                answer=True
            )
            self.validate_settings(step='api')
            api_generator = APIGenerator(app_label)

            if cache_support == 'yes':
                reporter.add_question_answer(
                    question='cache support',
                    answer=True
                )
                check, message = api_generator.generate_api(diagram_path, True)
            else:
                reporter.add_question_answer(
                    question='cache support',
                    answer=False
                )
                check, message = api_generator.generate_api(diagram_path)

            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))
        else:
            reporter.add_question_answer(
                question='create serializers.py',
                answer=False
            )
            reporter.add_question_answer(
                question='create views.py',
                answer=False
            )

        if create_test == 'yes':
            reporter.add_question_answer(
                question='create test_api.py',
                answer=True
            )
            reporter.add_question_answer(
                question='create test_model.py',
                answer=True
            )
            self.validate_settings(step='test')
            test_generator = TestGenerator(app_label)
            check, message = test_generator.generate_tests(diagram_path)
            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))
        else:
            reporter.add_question_answer(
                question='create test_api.py',
                answer=False
            )
            reporter.add_question_answer(
                question='create test_model.py',
                answer=False
            )

        if docker_support == 'yes':
            reporter.add_question_answer(
                question='create docker-compose.yml',
                answer=True
            )
            reporter.add_question_answer(
                question='create Dockerfile',
                answer=True
            )
            version = input('Please enter the version of your project(e.g 2.1): ')
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

            docker_generator = DockerGenerator(
                app_label, version,
                db_image, db_name,
                db_user, db_pass,
                redis_support, rabbit_support,
                rabbit_user, rabbit_pass
            )

            check, message = docker_generator.generate()

            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))

            if not redis_support and cache_support:
                print("""
                hint: Add this setting to your settings.py

                REDIS_URL = 'redis://localhost:6379/'
                CACHES = {
                    "default": {
                    "BACKEND": "django_redis.cache.RedisCache",
                    "LOCATION": os.environ['REDIS_URL'] if os.environ.get('REDIS_URL') else settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else 'redis://localhost:6379/'
                    }
                }
                """)
        else:
            reporter.add_question_answer(
                question='create docker-compose.yml',
                answer=False
            )
            reporter.add_question_answer(
                question='create Dockerfile',
                answer=False
            )

        for message in stdout_messages:
            self.stdout.write(message)
