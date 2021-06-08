from decouple import config
from django.conf import settings

from .base import (
    INSTALLED_APPS,
    STATIC_ROOT, BASE_DIR, STATICFILES_DIRS
)

# ############## #
#   EXTENSIONS   #
# ############## #

# admin
INSTALLED_APPS.append('django.contrib.admindocs')
INSTALLED_APPS.append('django.contrib.sites')

# packages
INSTALLED_APPS.append('rest_framework')
INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS.append('drf_yasg')
INSTALLED_APPS.append('django_seed')

# Applications
INSTALLED_APPS.append('generator')

# Sample apps
INSTALLED_APPS.append('products')

# ###################### #
#     REST FRAMEWORK     #
# ###################### #

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
########### #
#  CACHE    #
########### #
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_HOST')
    }
}
