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

PUBNUB_PUBLISH_KEY = 'pub-c-99d402d4-9ece-4f63-a7ba-6c3ec61d36b4'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-ba289054-825e-11e2-9881-12313f022c90'
PUBNUB_SECRET_KEY = 'sec-c-M2NiZjBjMWYtMWIyNC00MjIyLWJhYjAtNGZhY2IxNDQxZmEx'
