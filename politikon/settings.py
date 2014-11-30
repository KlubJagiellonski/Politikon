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

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jakub Lipinski', 'jakub.lipinski@gmail.com'),
    ('Tomasz Grynfelder', 't.grynfelder@gmail.com')
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Warsaw'
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
FACEBOOK_APPLICATION_INITIAL_PERMISSIONS = ['publish_actions', 'publish_stream', 'user_relationships']

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

CELERY_SEND_EVENTS = True
CELERY_TASK_RESULT_EXPIRES = 10
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_IMPORTS = ("accounts.tasks", "canvas.tasks", "events.tasks")

CELERYBEAT_SCHEDULE = {
    'update_portfolio_values': {
        'task': 'accounts.tasks.update_portfolio_value',
        'schedule': timedelta(minutes=1)
    },
    'create_hourly_open_events_snapshot': {
        'task': 'events.tasks.create_open_events_snapshot',
        'schedule': crontab(minute=11)
    },
    'create_hourly_accounts_snapshot': {
        'task': 'accounts.tasks.create_accounts_snapshot',
        'schedule': crontab(minute=31)
    },
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

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
# CONSTANCE_DATABASE_CACHE_BACKEND = 'default' # prior to changes in django-constances

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

ASSETS_ROOT = DJANGO_PROJECT_ROOT / 'static'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django_assets.finders.AssetsFinder',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAIYVO7SIW5CILJWBQ')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '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')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'pltn')
AWS_S3_HOST = os.environ.get('AWS_S3_HOST', 'pltn.s3-website.eu-central-1.amazonaws.com')
AWS_QUERYSTRING_AUTH = False

STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
ASSETS_AUTO_BUILD = False

import boto.s3.connection
AWS_S3_CALLING_FORMAT = boto.s3.connection.OrdinaryCallingFormat()

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@2@yw=u4h152#iscro&(4pcka%m1eydvw=_sne)@10f9+t^g9='

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
    # forcing one hostname on production
    'politikon.modules.HostnameRedirectMiddleware',
    # forcing SSL using https://github.com/rdegges/django-sslify. This need to be the first middleware
    'sslify.middleware.SSLifyMiddleware',
    # adding basic auth
    'politikon.modules.BasicAuthMiddleware',
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

# needed by SSLify
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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

    'coffin',
    'django_assets',

    'constance',
    'constance.backends.database',
    'djcelery',
    'fandjango',
    'gunicorn',
    'south',

    'accounts',
    'bladepolska',
    'canvas',
    'events',
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
