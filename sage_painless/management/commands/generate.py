import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from sage_painless.services.model_generator import ModelGenerator
from sage_painless.services.admin_generator import AdminGenerator
from sage_painless.services.api_generator import APIGenerator
from sage_painless.services.test_generator import TestGenerator
from sage_painless.utils.json_service import JsonHandler
from sage_painless.utils.report_service import ReportUserAnswer
from sage_painless.validators.diagram_validator import DiagramValidator


class Command(BaseCommand, JsonHandler, DiagramValidator):
    APPS_KEYWORD = 'apps'
    help = 'Generate all files need to your new apps.'

    def add_arguments(self, parser):
        """initialize arguments"""
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
        diagram_path = options.get('diagram')
        diagram = self.load_json(diagram_path)
        self.validate_all(diagram)  # validate diagram
        stdout_messages = list()
        for app_name in diagram.get(self.APPS_KEYWORD).keys():
            create_model = input(f'Would you like to generate models.py for {app_name} app (yes/no)? ')
            create_admin = input(f'Would you like to generate admin.py for {app_name} app (yes/no)? ')
            create_api = input(f'Would you like to generate serializers.py & views.py for {app_name} app (yes/no)? ')
            create_test = input(f'Would you like to generate test for {app_name} app (yes/no)? ')
            cache_support = input(f'Would you like to add cache queryset support for {app_name} app (yes/no)? ')

            reporter = ReportUserAnswer(
                app_name=app_name,
                file_prefix=f'{app_name}-{int(datetime.datetime.now().timestamp())}'
            )
            reporter.init_report_file()

            if create_model == 'yes':
                model_generator = ModelGenerator()
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
                    stdout_messages.append(self.style.SUCCESS(f'{app_name}[INFO]: {message}'))
                else:
                    stdout_messages.append(self.style.ERROR(f'{app_name}[ERROR]: {message}'))
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
                admin_generator = AdminGenerator()
                check, message = admin_generator.generate(diagram_path)
                if check:
                    stdout_messages.append(self.style.SUCCESS(f'{app_name}[INFO]: {message}'))
                else:
                    stdout_messages.append(self.style.ERROR(f'{app_name}[ERROR]: {message}'))
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
                api_generator = APIGenerator()

                if cache_support == 'yes':
                    print("""
                    hint: This setting should be in settings.py

                    REDIS_URL = 'redis://localhost:6379/'
                    CACHES = {
                        "default": {
                        "BACKEND": "django_redis.cache.RedisCache",
                        "LOCATION": os.environ['REDIS_URL'] if os.environ.get('REDIS_URL') else settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else 'redis://localhost:6379/'
                        }
                    }
                    """)
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
                    stdout_messages.append(self.style.SUCCESS(f'{app_name}[INFO]: {message}'))
                else:
                    stdout_messages.append(self.style.ERROR(f'{app_name}[ERROR]: {message}'))
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
                test_generator = TestGenerator()
                check, message = test_generator.generate_tests(diagram_path)
                if check:
                    stdout_messages.append(self.style.SUCCESS(f'{app_name}[INFO]: {message}'))
                else:
                    stdout_messages.append(self.style.ERROR(f'{app_name}[ERROR]: {message}'))
            else:
                reporter.add_question_answer(
                    question='create test_api.py',
                    answer=False
                )
                reporter.add_question_answer(
                    question='create test_model.py',
                    answer=False
                )

        for message in stdout_messages:
            self.stdout.write(message)
