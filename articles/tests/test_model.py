"""
Auto Generated test
You may need to change some parts
"""
from rest_framework.test import APITestCase
from django_seed import Seed

from articles.models import *

seeder = Seed.seeder()


class ArticlesModelTest(APITestCase):
    """
    articles Model Test
    Auto Generated
    """

    def setUp(self) -> None:
        pass

    def test_article_model(self):
        """
        test Article creation
        """
        seeder.add_entity(Article, 1)
        seeder.execute()  # create instance
        # assertions
        self.assertTrue(Article.objects.exists())
