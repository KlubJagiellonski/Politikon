import dj_database_url
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2

ALLOWED_HOSTS = ['www.politikon.org.pl', 'politikon.org.pl']
CATCHALL_REDIRECT_HOSTNAME = 'www.politikon.org.pl'

DATABASES = {'default': dj_database_url.config()}

FACEBOOK_APPLICATION_ID = os.environ.get("FACEBOOK_APPLICATION_ID", "208090085996947")
FACEBOOK_APPLICATION_SECRET_KEY = os.environ.get("FACEBOOK_APPLICATION_SECRET_KEY", "15b8095d73be74cf072f0596325fbb67")
FACEBOOK_APPLICATION_NAMESPACE = os.environ.get("FACEBOOK_APPLICATION_NAMESPACE", "politikon")

FACEBOOK_REALTIME_VERIFY_TOKEN = "jkwjknvkjfwelnvljknsknv"

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", "07cM50zfHeEZg2uuN0lkyyC4w")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", "NQE2HRp135fn4rQSxvdMdcZ4Ug3HzG8wwhoKGGUjtxbFVk8Id4")
FACEBOOK_APP_ID = FACEBOOK_APPLICATION_ID
FACEBOOK_API_SECRET = FACEBOOK_APPLICATION_SECRET_KEY
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID", "579638841369-9c8cliqj8o73nbufdbvfc144pqt81uc9.apps.googleusercontent.com")
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET", "vUbknd9cRgqEIu4yZlgk4Yo9")

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
if 'MEMCACHIER_USERNAME' in os.environ and 'MEMCACHIER_PASSWORD' in os.environ:
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

BASICAUTH = True
BASICAUTH_USERNAME = 'stawiamy'
BASICAUTH_PASSWORD = 'napolityke'