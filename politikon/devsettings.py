import os
from path import path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

DJANGO_PROJECT_ROOT = path(__file__).abspath().dirname().dirname()

MEDIA_ROOT = DJANGO_PROJECT_ROOT / 'static' / 'uploads'
MEDIA_URL = '/static/uploads/'

ALLOWED_HOSTS = ['localhost', '192.168.59.103']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVE_STATIC_FILES = False
CELERY_ALWAYS_EAGER = True

# Since below these are test app settings, it should be safe to open-source it
FACEBOOK_APPLICATION_ID = "134939156680151"
FACEBOOK_APPLICATION_SECRET_KEY = "ce45e3ce267cd64a5cfee9743fc28d59"
FACEBOOK_APPLICATION_NAMESPACE = "politikon_staging"

# Since below these are test app settings, it should be safe to open-source it
TWITTER_CONSUMER_KEY = "7k5NfWvH6FFKloAa3BkZx6XpG"
TWITTER_CONSUMER_SECRET = "1ZbxNN6B3I1A8JRnSW1F7uKWWX96kGNPYkuOGwE8lTh4fdi6m5"

# social_auth configuration
SOCIAL_AUTH_TWITTER_KEY = TWITTER_CONSUMER_KEY
SOCIAL_AUTH_TWITTER_SECRET = TWITTER_CONSUMER_SECRET
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_APPLICATION_ID
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_APPLICATION_SECRET_KEY
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# sandbox keys
PUBNUB_PUBLISH_KEY = 'pub-c-c852ffa1-72fc-41ed-9720-2f88b0e54880'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-e8bd5ce2-8506-11e2-ac19-12313f022c90'
PUBNUB_SECRET_KEY = 'sec-c-ZmE0OTc5MDYtYWUxNi00YTJjLWFjOGMtODVhNGQ5Y2JmNTdj'
PUBNUB_IS_SSL = False


DATABASE_URL = 'postgres://postgres:postgres@' + os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ':' + os.environ['POSTGRES_PORT_5432_TCP_PORT']  + '/' + 'politikon'

#disabling SSL on local
SSLIFY_DISABLE = True
