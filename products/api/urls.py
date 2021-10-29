"""
Auto Generated urls.py
Automatically generated with ❤️ by django-sage-painless
"""

from rest_framework.routers import DefaultRouter

from products.api.views import (
    CategoryViewset,
    ProductViewset,
    DiscountViewset,

)

router = DefaultRouter()

router.register(r'category', CategoryViewset, basename='category')

router.register(r'product', ProductViewset, basename='product')

router.register(r'discount', DiscountViewset, basename='discount')

urlpatterns = router.urls
