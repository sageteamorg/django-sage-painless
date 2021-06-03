import os
from datetime import timedelta

from Crypto import Random
from Crypto.PublicKey import RSA
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
# INSTALLED_APPS.append('rest_framework_simplejwt.token_blacklist')
INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS.append('drf_yasg')
INSTALLED_APPS.append('django_seed')
# INSTALLED_APPS.append('django_celery_beat')
# INSTALLED_APPS.append('safedelete')
# INSTALLED_APPS.append('sorl.thumbnail')
# INSTALLED_APPS.append('django_filters')
# INSTALLED_APPS.append('colorfield')
# INSTALLED_APPS.append('admin_footer')
# INSTALLED_APPS.append('django_admin_logs')
# INSTALLED_APPS.append('silk')  # silk profiler

# Applications
INSTALLED_APPS.append('painless')
# INSTALLED_APPS.append('users')
INSTALLED_APPS.append('upload_center')
INSTALLED_APPS.append('api')
INSTALLED_APPS.append('articles')
INSTALLED_APPS.append('generator')
INSTALLED_APPS.append('products')
# INSTALLED_APPS.append('authentication')
# INSTALLED_APPS.append('education')
# INSTALLED_APPS.append('subscription')
# INSTALLED_APPS.append('practice')
# INSTALLED_APPS.append('project')
# INSTALLED_APPS.append('progression')
# INSTALLED_APPS.append('skill')
# INSTALLED_APPS.append('payment')
# INSTALLED_APPS.append('discount')
# INSTALLED_APPS.append('ticket')
# INSTALLED_APPS.append('cms')
# INSTALLED_APPS.append('stream')

# ###################### #
#     REST FRAMEWORK     #
# ###################### #

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # react, oauth
        'rest_framework.authentication.TokenAuthentication',  # mobile devices
        # 'rest_framework.authentication.SessionAuthentication',  # web based
    ],
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_THROTTLE_RATES': {
        'check_membership_existence_anon': '5/day',
        'anon_otp': '1/minute',
        'user_otp': '1/minute',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
#
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'UPDATE_LAST_LOGIN': True,
#
#     'ALGORITHM': 'RS512',
#     'SIGNING_KEY': open(os.path.join(BASE_DIR, 'jwt-key')).read(),
#     'VERIFYING_KEY': open(os.path.join(BASE_DIR, 'jwt-key.pub')).read(),
#     'AUDIENCE': 'Student',
#     'ISSUER': 'Theivan.org',
#
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
#     'USER_ID_FIELD': 'username',
#     'USER_ID_CLAIM': 'identity',
#
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
#
#     'JTI_CLAIM': 'jti',
#
#     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
#     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
# }

# #################### #
#   BACKGROUND TASKS   #
# #################### #
BACKGROUND_TASK_RUN_ASYNC = True

# ########### #
#   CELERY    #
# ########### #
# CELERY_BROKER_URL = config('CELERY_BROKER_URL')
# CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# # CELERY_TASK_QUEUES = {
# #     'default': {
# #         "exchange": "default",
# #         "binding_key": "default",
# #     },
# #     'otp': {
# #         'exchange': 'otp',
# #         'routing_key': 'otp',
# #     }
# # }
# CELERY_TASK_ROUTES = {
#     'authentication.tasks.send_otp': {'queue': 'otp'}
# }
# CELERY_ENABLE_UTC = True
# CELERY_TIMEZONE = 'UTC'


########### #
#  CACHE    #
########### #
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_HOST')
    }
}
# CACHE_QUERYSET_ENABLED = True
# # CACHE_PAGE_ENABLED = True
# # CACHE_PAGE_PER_SITE_PREFIX = 'view'
# # should pass 1 argument (user) and return seconds in integer
# CACHE_PER_USER_TIMEOUT_FUNC = 'painless.utils.cache.services.timeout_handlers.get_subscription_timedelta'
# CACHE_PER_USER_UNIQUE_ATTR = 'id'
# CACHE_TIMEOUT = 3600
# PRIVATE_KEY = RSA.generate(256*4, Random.new().read)
# PUBLIC_KEY = PRIVATE_KEY.publickey()


# ########### #
#   UPLOAD    #
# ########### #
# FILE_UPLOAD_HANDLERS = [
#     'painless.utils.handlers.upload.ChunkFileUploadHandler'
# ]
# UPLOAD_CHUNK_SIZE = 2500 * 2 ** 10  # 2500 KB

# ######################### #
#       AdminInterface      #
# ######################### #
from datetime import datetime

ADMIN_FOOTER_DATA = {
    'site_url': 'https://www.sageteam.org',
    'site_name': 'S.A.G.E. Team',
    'period': '{}'.format(datetime.now().year),
    'version': 'v1.0.0 - production'
}

# #################### #
# IMPORTANT VARIABLES  #
# #################### #

# LOGIN_REDIRECT_URL = '/portal'
# LOGIN_URL = '/auth/login'
# LOGOUT_REDIRECT_URL = '/'
# AUTH_USER_MODEL = 'users.User'

# ######################### #
#       Code Generator      #
# ######################### #

# DB information should be in settings.ini too
ABSTRACT_DB_NAME = 'abstract_postgres'
ABSTRACT_DB_HOST = 'localhost'
ABSTRACT_DB_PORT = 5432
ABSTRACT_DB_USER = 'postgres'
ABSTRACT_DB_PASS = 'mehran8282'

PROJECTS_DIR = 'projects'
