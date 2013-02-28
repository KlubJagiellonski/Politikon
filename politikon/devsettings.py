import os
from path import path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DJANGO_PROJECT_ROOT = path(__file__).abspath().dirname().dirname()

MEDIA_ROOT = DJANGO_PROJECT_ROOT / 'static' / 'uploads'
MEDIA_URL = '/static/uploads/'

ALLOWED_HOSTS = ['localhost']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
CONSTANCE_REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVE_STATIC_FILES = True

FACEBOOK_APPLICATION_ID = "134939156680151"
FACEBOOK_APPLICATION_SECRET_KEY = "ce45e3ce267cd64a5cfee9743fc28d59"
FACEBOOK_APPLICATION_NAMESPACE = "politikon_staging"
