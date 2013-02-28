import dj_database_url
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {'default': dj_database_url.config()}

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
if 'MEMCACHIER_USERNAME' in os.environ and 'MEMCACHE_PASSWORD' in os.environ:
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

    CACHES = {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';'),
        'TIMEOUT': 600,
        'BINARY': True,
      }
    }
else:
    CACHES = {
      'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';'),
        'TIMEOUT': 600,
        'BINARY': True,
      }
    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = os.environ.get('MAILGUN_USERNAME', '')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_PASSWORD', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SERVE_STATIC_FILES = True

FACEBOOK_APP_ID = "134939156680151"
FACEBOOK_API_SECRET = "ce45e3ce267cd64a5cfee9743fc28d59"
