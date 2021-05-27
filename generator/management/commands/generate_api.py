from django.core.management.base import BaseCommand

from generator.services.api_generator import APIGenerator


class Command(BaseCommand):
    help = 'Generate serializers.py and views.py for given app'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--app', type=str, help='app label that will generate admin.py for')
        parser.add_argument('-d', '--diagram', type=str, help='diagram that will generate admin.py for')

    def handle(self, *args, **options):
        app_label = options.get('app')
        diagram_path = options.get('diagram')
        api_generator = APIGenerator(app_label)
        generated, message = api_generator.generate_api(diagram_path)
        if generated:
            self.stdout.write(
                self.style.SUCCESS(message)
            )
        else:
            self.stdout.write(
                self.style.ERROR(message)
            )
