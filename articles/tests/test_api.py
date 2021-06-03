"""
Auto Generated test
You may need to change some parts
"""
from django.urls import reverse
from rest_framework.test import APITestCase
from django_seed import Seed

from articles.models import *

seeder = Seed.seeder()


class ArticlesAPITest(APITestCase):
    """
    articles API Test
    Auto Generated
    """

    def setUp(self) -> None:

        seeder.add_entity(Article, 3)

        seeder.execute()  # create instances

    def test_article_list_success(self):
        """
        test Article list
        """
        url = reverse('article-list')
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        if response.data.get('count'):
            self.assertGreater(response.data['count'], 0)
        self.assertGreater(len(response.data), 0)

    def test_article_detail_success(self):
        """
        test Article detail
        """
        article = Article.objects.first()
        url = reverse('article-detail', args=[article.pk])
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get('title'), article.title)

        self.assertEqual(response.data.get('body'), article.body)

        self.assertEqual(response.data.get('slug'), article.slug)

        self.assertEqual(response.data.get('options'), article.options)
