import datetime

from django.core.management import BaseCommand

from sage_painless.services.readme_generator import ReadMeGenerator
from sage_painless.utils.report_service import ReportUserAnswer


class Command(BaseCommand):
    help = 'Generate all docs.'

    def add_arguments(self, parser):
        """initialize arguments"""
        parser.add_argument('-d', '--diagram', type=str, help='sql diagram path that will make models.py from it')
        parser.add_argument('-g', '--git', type=bool, help='generate git commits')

    def handle(self, *args, **options):
        diagram_path = options.get('diagram')
        git_support = options.get('git', False)
        stdout_messages = list()
        docs_support = input('Would you like to generate README.md(yes/no)? ')

        reporter = ReportUserAnswer(
            app_name='docs',
            file_prefix=f'docs-{int(datetime.datetime.now().timestamp())}'
        )
        reporter.init_report_file()

        if docs_support == 'yes':
            reporter.add_question_answer(
                question='create README',
                answer=True
            )
            readme_generator = ReadMeGenerator()
            check, message = readme_generator.generate(diagram_path, git_support=git_support)
            if check:
                stdout_messages.append(self.style.SUCCESS(f'docs[INFO]: {message}'))
            else:
                stdout_messages.append(self.style.ERROR(f'docs[ERROR]: {message}'))
        else:
            reporter.add_question_answer(
                question='create README',
                answer=False
            )

        for message in stdout_messages:
            self.stdout.write(message)
