from rest_framework.routers import DefaultRouter

from api.api.views import *

router = DefaultRouter()

router.register(r'user', UserViewset, basename='user')

router.register(r'profile', ProfileViewset, basename='profile')

urlpatterns = router.urls
