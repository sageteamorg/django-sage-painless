from django.core.management.base import BaseCommand

from generator.services.admin_generator import AdminGenerator


class Command(BaseCommand):
    help = 'Generate admin.py for given app'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--app', type=str, help='app label that will generate admin.py for')

    def handle(self, *args, **options):
        app_label = options.get('app')
        admin_generator = AdminGenerator(app_label)
        generated = admin_generator.generate()
        if generated:
            self.stdout.write(
                self.style.SUCCESS('admin.py generated successfully for app {}'.format(app_label))
            )
        else:
            self.stdout.write(
                self.style.ERROR('Error in generating admin.py')
            )
