from django.test import TestCase
from django.apps import apps

from sage_painless.services.readme_generator import ReadMeGenerator


class TestReadMeGenerator(TestCase):
    def setUp(self) -> None:
        self.readme_generator = ReadMeGenerator()

    def test_get_built_in_apps(self):
        """test get django built-in packages"""
        built_in_apps = [app.verbose_name for app in apps.get_app_configs() if app.name.startswith('django.')]
        read_me_apps = self.readme_generator.get_built_in_app_names()

        self.assertListEqual(read_me_apps, built_in_apps)

    def test_get_other_apps(self):
        """test get apps exclude built-in apps"""
        other_apps = [app.verbose_name for app in apps.get_app_configs() if not app.name.startswith('django.')]
        read_me_apps = self.readme_generator.get_installed_module_names()

        self.assertListEqual(read_me_apps, other_apps)
