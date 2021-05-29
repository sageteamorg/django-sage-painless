from django.core.management.base import BaseCommand

from generator.services.test_generator import TestGenerator


class Command(BaseCommand):
    help = 'Generate test for given app via diagram file.'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--app', type=str, help='app label that will generate models.py for')
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path that will make models.py from it')

    def handle(self, *args, **options):
        app_label = options.get('app')
        diagram_path = options.get('diagram')
        test_generator = TestGenerator(app_label)
        generated, message = test_generator.generate_tests(
            diagram_path=diagram_path
        )
        if generated:
            self.stdout.write(
                self.style.SUCCESS(message)
            )
        else:
            self.stdout.write(
                self.style.ERROR(message)
            )
