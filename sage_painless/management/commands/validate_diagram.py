from django.core.management.base import BaseCommand

from sage_painless.utils.json_service import JsonHandler
from sage_painless.validators.diagram_validator import DiagramValidator


class Command(BaseCommand, JsonHandler, DiagramValidator):
    help = 'Generate all files need to your new apps.'

    def add_arguments(self, parser):
        """initialize arguments"""
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path')

    def handle(self, *args, **options):
        """get configs from user and generate"""
        diagram_path = options.get('diagram')
        diagram = self.load_json(diagram_path)

        self.validate_all(diagram)

        self.stdout.write(
            self.style.SUCCESS('system check completed with [0] error')
        )
