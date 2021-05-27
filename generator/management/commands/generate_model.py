from django.core.management.base import BaseCommand

from generator.services.model_generator import ModelGenerator


class Command(BaseCommand):
    help = 'Generate models.py for given app via sql diagram file.'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--app', type=str, help='app label that will generate models.py for')
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path that will make models.py from it')

    def handle(self, *args, **options):
        app_label = options.get('app')
        diagram_path = options.get('diagram')
        model_generator = ModelGenerator(app_label)
        generated, message = model_generator.generate_models(
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
