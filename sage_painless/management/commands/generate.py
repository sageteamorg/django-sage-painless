from django.core.management.base import BaseCommand
from django.conf import settings

from sage_painless.services.model_generator import ModelGenerator
from sage_painless.services.admin_generator import AdminGenerator
from sage_painless.services.api_generator import APIGenerator
from sage_painless.services.test_generator import TestGenerator
from sage_painless.services.docker_generator import DockerGenerator


class Command(BaseCommand):
    help = 'Generate all files need to your new app.'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--app', type=str, help='app label that will generate models.py for')
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path that will make models.py from it')

    def validate_settings(self):
        if not 'sage_painless' in settings.INSTALLED_APPS:
            raise IOError('Add `sage_painless` to your INSTALLED_APPS')
        
        if not 'rest_framework' in settings.INSTALLED_APPS:
            raise IOError('Add `rest_framework` to your INSTALLED_APPS')
        
        if not 'drf_yasg' in settings.INSTALLED_APPS:
            raise IOError('Add `drf_yasg` to your INSTALLED_APPS')
        
        if not 'django_seed' in settings.INSTALLED_APPS:
            raise IOError('Add `django_seed` to your INSTALLED_APPS')


    def handle(self, *args, **options):
        self.validate_settings()

        app_label = options.get('app')
        diagram_path = options.get('diagram')
        create_model = input('Would you like to generate models.py(yes/no)? ')
        create_admin = input('Would you like to generate admin.py(yes/no)? ')
        create_api = input('Would you like to generate serializers.py & views.py(yes/no)? ')
        create_test = input('Would you like to generate test for your project(yes/no)? ')
        cache_support = input('Would you like to add cache queryset support(yes/no)? ')
        docker_support = input('Would you like to dockerize your project(yes/no)? ')

        stdout_messages = list()

        if create_model == 'yes':
            model_generator = ModelGenerator(app_label)

            if cache_support == 'yes':
                check, message = model_generator.generate_models(diagram_path, True)
            else:
                check, message = model_generator.generate_models(diagram_path)

            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))

        if create_admin == 'yes':
            admin_generator = AdminGenerator(app_label)
            check, message = admin_generator.generate(diagram_path)
            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))

        if create_api == 'yes':
            api_generator = APIGenerator(app_label)

            if cache_support == 'yes':
                check, message = api_generator.generate_api(diagram_path, True)
            else:
                check, message = api_generator.generate_api(diagram_path)

            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))

        if create_test == 'yes':
            test_generator = TestGenerator(app_label)
            check, message = test_generator.generate_tests(diagram_path)
            if check:
                stdout_messages.append(self.style.SUCCESS(message))
            else:
                stdout_messages.append(self.style.ERROR(message))

        if docker_support == 'yes':
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
                rabbit_user = input('Please enter rabbitMQ user username: ')
                rabbit_pass = input('Please enter rabbitMQ user password: ')

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

        for message in stdout_messages:
            self.stdout.write(message)
