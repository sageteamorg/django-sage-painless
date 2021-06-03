"""
Auto Generated views.py
You may need to change some parts
"""
from rest_framework.viewsets import ModelViewSet

from articles.models import *
from articles.api.serializers import *


class ArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
