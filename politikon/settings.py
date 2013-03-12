from celery.schedules import crontab
from datetime import timedelta
import dj_database_url
import os
from path import path
import urlparse
import sys

DJANGO_PROJECT_ROOT = path(__file__).abspath().dirname().dirname()

# ENV-defined settings
FACEBOOK_APPLICATION_ID = os.environ.get('FACEBOOK_APPLICATION_ID')
FACEBOOK_APPLICATION_SECRET_KEY = os.environ.get('FACEBOOK_APPLICATION_SECRET_KEY')
FACEBOOK_APPLICATION_NAMESPACE = os.environ.get('FACEBOOK_APPLICATION_NAMESPACE')

PUBNUB_PUBLISH_KEY = os.environ.get('PUBNUB_PUBLISH_KEY')
PUBNUB_SUBSCRIBE_KEY = os.environ.get('PUBNUB_SUBSCRIBE_KEY')
PUBNUB_SECRET_KEY = os.environ.get('PUBNUB_SECRET_KEY')
PUBNUB_IS_SSL = False

# Django settings for politikon project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Tomek Kopczuk', 'tomek@bladepolska.com'),
    ('MArcin Mincer', 'marcin@bladepolska.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'pl'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'

FACEBOOK_APPLICATION_CANVAS_URL = '/canvas'
FANDJANGO_ENABLED_PATHS = [
    '^canvas/(.*)',
]
FANDJANGO_CACHE_SIGNED_REQUEST = True

ASSETS_MANIFEST = "file:"

REDIS_BASE_URL = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')
REDIS_PARAMS = urlparse.urlparse(REDIS_BASE_URL)

# Celery config

REDIS_HOST = REDIS_PARAMS.hostname
REDIS_PORT = REDIS_PARAMS.port
REDIS_DB = 0
REDIS_CONNECT_RETRY = True

BROKER_URL = REDIS_BASE_URL + "/0"
CELERY_RESULT_BACKEND = REDIS_BASE_URL + "/0"

CELERY_CONCURRENCY = 2
CELERY_SEND_EVENTS = True
CELERY_TASK_RESULT_EXPIRES = 10
CELERY_IGNORE_RESULT = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_IMPORTS = ("canvas.tasks", "accounts.tasks")


CELERYBEAT_SCHEDULE = {
    'consume_facebook_user_sync_task': {
        'task': 'canvas.tasks.consume_facebook_user_sync_task',
        'schedule': timedelta(minutes=5)
    },
    'consume_facebook_user_friends_sync_task': {
        'task': 'canvas.tasks.consume_facebook_user_friends_sync_task',
        'schedule': timedelta(minutes=5)
    },
    'consume_publish_activities_tasks': {
        'task': 'canvas.tasks.consume_publish_activities_tasks',
        'schedule': timedelta(minutes=5)
    },
    'topup_accounts_task': {
        'task': 'accounts.tasks.topup_accounts_task',
        'schedule': crontab(minute=0, hour=0)
    },
}

CONSTANCE_REDIS_CONNECTION = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': 0,
}
if REDIS_PARAMS.password:
    CONSTANCE_REDIS_CONNECTION['password'] = REDIS_PARAMS.password
    BROKER_PASSWORD = REDIS_PARAMS.password

CONSTANCE_CONFIG = {
    'PUBLISH_DELAY_IN_MINUTES': (10.0, 'minutes of delay between action and it\'s publication'),
    'STARTING_CASH': (1000.0, 'cash for start'),
    'SMALL_EVENT_IMAGE_WIDTH': (365, 'small event image width'),
    'SMALL_EVENT_IMAGE_HEIGHT': (255, 'small event image height'),
    'BIG_EVENT_IMAGE_WIDTH': (715, 'big event image width'),
    'BIG_EVENT_IMAGE_HEIGHT': (300, 'big event image height'),
    'DAILY_TOPUP': (100, 'daily cash topup'),
}

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = DJANGO_PROJECT_ROOT / 'static_build'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations
TEMPLATE_DIRS = (
    DJANGO_PROJECT_ROOT / 'templates',
)

STATICFILES_DIRS = (
    DJANGO_PROJECT_ROOT / 'static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@2@yw=u4h152#iscro&(4pcka%m1eydvw=_sne)@10f9+t^g9='

from constance import config

JINJA2_GLOBALS = {
    'config': config
}

JINJA2_EXTENSIONS = [
    'webassets.ext.jinja2.AssetsExtension',
    'jinja2.ext.with_',
    'jinja2.ext.do',
    'jinja2.ext.i18n',
    'jinja2.ext.loopcontrols',
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'bladepolska.context_processors.settings',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    'canvas.backends.FacebookCanvasFandjangoBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    # 'bladepolska.middleware.InstrumentMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'canvas.middleware.FacebookMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'politikon.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'politikon.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'accounts',
    'bladepolska',
    'canvas',
    'events',

    'coffin',
    'django_assets',

    'constance',
    'djcelery',
    'fandjango',
    'gunicorn',
    'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)-12s] [%(levelname)s] %(message)s',
            'datefmt': '%b %d %H:%M:%S'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'politikon': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

import smartsettings
# @TODO: add ensure_exists('<setting name>') to django-smartsettings
smartsettings.config(globals(), {
    'FLAVOURS': (
        'TESTING',
        'DEV',
        'PRODUCTION',
    ),
    'DEFAULT': 'DEV'  # default flavour always loads localsettings.py!
})
