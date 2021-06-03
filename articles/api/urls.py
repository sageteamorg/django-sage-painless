"""
Auto Generated urls.py
You may need to change some parts
"""
from rest_framework.routers import DefaultRouter

from articles.api.views import *

router = DefaultRouter()

router.register(r'article', ArticleViewset, basename='article')

urlpatterns = router.urls
