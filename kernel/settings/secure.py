import os
from .base import BASE_DIR
from decouple import config


SECRET_KEY = config('SECRET_KEY')
PREPEND_WWW = config('PREPEND_WWW', cast = bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
        'TEST': {
            'NAME': config('DB_TEST'),
            'CHARSET': config('DB_CHARSET'),
        },
    },
    'abstract_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('ABSTRACT_DB_NAME'),
        'USER': config('ABSTRACT_DB_USER'),
        'PASSWORD': config('ABSTRACT_DB_PASS'),
        'HOST': config('ABSTRACT_DB_HOST'),
        'PORT': config('ABSTRACT_DB_PORT'),
    }
}

# ######################### #
#           EMAIL           #
# ######################### #

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)


# ######################### #
#      UPLOAD SETTING       #
# ######################### #

FILE_UPLOAD_TEMP_DIR = config('FILE_UPLOAD_TEMP_DIR')
FILE_UPLOAD_PERMISSIONS = 0o755
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_MAX_MEMORY_SIZE = config('FILE_UPLOAD_MAX_MEMORY_SIZE', cast=int)
MAX_UPLOAD_SIZE = config('MAX_UPLOAD_SIZE', cast=int)


# ############################ #
#      SSL CONFIGURATION       #
# ############################ #
SECURE_BROWSER_XSS_FILTER=config('SECURE_BROWSER_XSS_FILTER', cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF=config('SECURE_CONTENT_TYPE_NOSNIFF', cast=bool)
SECURE_HSTS_INCLUDE_SUBDOMAINS=config('SECURE_HSTS_INCLUDE_SUBDOMAINS', cast=bool)
SECURE_HSTS_PRELOAD=config('SECURE_HSTS_PRELOAD', cast=bool)
SECURE_HSTS_SECONDS=config('SECURE_HSTS_SECONDS', cast=int)

if config('SECURE_PROXY_SSL_HEADER', cast=bool):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_REDIRECT_EXEMPT=[]
SECURE_REFERRER_POLICY=config('SECURE_REFERRER_POLICY')
SECURE_SSL_HOST=config('SECURE_SSL_HOST')
SECURE_SSL_REDIRECT=config('SECURE_SSL_REDIRECT', cast=bool)

# ############################ #
#           Security           #
# ############################ #
CSRF_COOKIE_AGE = config('CSRF_COOKIE_AGE', cast = int)
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', cast = bool)
CSRF_COOKIE_NAME = config('CSRF_COOKIE_NAME')
CSRF_COOKIE_PATH = config('CSRF_COOKIE_PATH')
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE').capitalize()
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast = bool)
CSRF_USE_SESSIONS = config('CSRF_USE_SESSIONS', cast = bool)
CSRF_HEADER_NAME = config('CSRF_HEADER_NAME')

# ######################### #
#       OTP SETTING         #
# ######################### #
IRAN_OTP_SECRET_KEY = config('IRAN_OTP_SECRET_KEY')
IRAN_OTP_USER_API_KEY = config('IRAN_OTP_USER_API_KEY')
IRAN_OTP_TEMPLATE_ID = config('IRAN_OTP_TEMPLATE_ID')

# ############################ #
#          Monitoring          #
# ############################ #

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'formatters': {
        'basic': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'advance': {
            'format': '{levelname}: [{asctime}] `{message}` | from_module: {module} | p={process:d} t={thread:d} ',
            'style': '{',
        },
    },

    'handlers': {
        'development': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'formatter': 'basic',
        },

        'production': {
            'level': config('DEBUG_PRODUCTION_LEVEL').upper(),
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, config('DEBUG_PRODUCTION_FILE')),
            'filters': ['require_debug_true'],
            'formatter': 'advance'
        },

        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }

    },

    'loggers': {
        'django': {
            'handlers': ['production', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        # root
        '': {
            'handlers': ['development'],
            'level': 'INFO',
            'propagate': False,
        },
    },

}


CACHE_TTL = 60 * 15


# ######################### #
#           EMAIL           #
# ######################### #

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

