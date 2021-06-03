"""
Auto Generated serializers.py
You may need to change some parts
"""
from rest_framework.serializers import ModelSerializer

from articles.models import *


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'slug',
            'created',
            'publish',
            'updated',
            'options',

        ]
