"""
Auto Generated urls.py
You may need to change some parts
"""
from rest_framework.routers import DefaultRouter

from products.api.views import *

router = DefaultRouter()

router.register(r'category', CategoryViewset, basename='category')

router.register(r'product', ProductViewset, basename='product')

router.register(r'discount', DiscountViewset, basename='discount')

urlpatterns = router.urls
