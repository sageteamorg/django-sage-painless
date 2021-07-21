import json
import os
from pathlib import Path

from django.conf import settings


class ReportUserAnswer:
    def __init__(self, app_name, file_prefix):
        self.file_prefix = file_prefix
        self.app_label = app_name

    def create_dir_is_not_exists(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

    def create_file_is_not_exists(self, file_path):
        if not os.path.isfile(file_path):
            file = Path(file_path)
            file.touch(exist_ok=True)

    def init_report_file(self):
        """create report file in docs dir"""
        self.create_dir_is_not_exists(f'{settings.BASE_DIR}/docs/')
        self.create_dir_is_not_exists(f'{settings.BASE_DIR}/docs/sage_painless/')
        self.create_dir_is_not_exists(f'{settings.BASE_DIR}/docs/sage_painless/report/')
        self.create_file_is_not_exists(
            f'{settings.BASE_DIR}/docs/sage_painless/report/{self.file_prefix}-generation-report.json'
        )

    def add_question_answer(self, question, answer):
        """append question answer to report file"""
        with open(f'{settings.BASE_DIR}/docs/sage_painless/report/{self.file_prefix}-generation-report.json', 'r+') as file:
            try:
                data = json.load(file)
            except:
                data = {}
            report = {
                question: answer
            }
            data.update(report)
            file.seek(0)
            json.dump(data, file)
