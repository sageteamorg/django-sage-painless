import os

from django.utils.translation import ugettext_lazy as _

from decouple import config

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'painless.utils.middlewares.cache_per_user_middleware.UpdateUserCacheMiddleware',
    # 'painless.utils.middlewares.cache_per_user_middleware.FetchFromUserCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'silk.middleware.SilkyMiddleware',  # silk profiler
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',

    # "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # "django_prometheus.middleware.PrometheusAfterMiddleware",

    # 'request.middleware.RequestMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

TEMPLATES_DIR = os.path.join(BASE_DIR, config('TEMPLATES_DIR'))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, os.path.join(BASE_DIR, config('DIRS'))],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                'apptemplates.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ROOT_URLCONF = 'kernel.urls'
WSGI_APPLICATION = 'kernel.wsgi.application'

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", _("English")),
    ("ar", _("Arabic")),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATIC_URL = config('STATIC_URL')

MEDIA_ROOT = os.path.join(BASE_DIR, config('MEDIA_UPLOAD_DIR'))

MEDIA_URL = config('MEDIA_URL')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, config('STATIC_DIR')),
)

STATIC_ROOT = os.path.join(BASE_DIR, config('COLLECT_STATIC_DIR'))

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SITE_ID = 1
