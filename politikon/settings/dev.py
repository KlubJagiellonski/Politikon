import dj_database_url
from .base import *

DEBUG = True

SITE_ID = 2

DJANGO_PROJECT_ROOT = path(__file__).abspath().dirname().dirname().dirname()

MEDIA_ROOT = DJANGO_PROJECT_ROOT / 'static' / 'uploads'
MEDIA_URL = 'https://politik.s3.amazonaws.com/'

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
FACEBOOK_APPLICATION_ID = "1623549301266280"
FACEBOOK_APPLICATION_SECRET_KEY = "aeadbbcf643847743b8ea9551b8b2986"
FACEBOOK_APPLICATION_NAMESPACE = "politikon_dev"

# Since below these are test app settings, it should be safe to open-source it
TWITTER_CONSUMER_KEY = "c96DyRfYWpIYTktS7CymHFNBJ"
TWITTER_CONSUMER_SECRET = "omcuLc58rqAYhvjis5FjgTqrH2mDoqFqRhwP9bhxlZuleQS6HL"

# oauth-tokens settings
# to keep in DB expired access tokens
OAUTH_TOKENS_HISTORY = True
OAUTH_TOKENS_TWITTER_CLIENT_ID = TWITTER_CONSUMER_KEY
OAUTH_TOKENS_TWITTER_CLIENT_SECRET = TWITTER_CONSUMER_SECRET
# user login
OAUTH_TOKENS_TWITTER_USERNAME = ''
# user password
OAUTH_TOKENS_TWITTER_PASSWORD = ''

# social_auth configuration
SOCIAL_AUTH_TWITTER_KEY = TWITTER_CONSUMER_KEY
SOCIAL_AUTH_TWITTER_SECRET = TWITTER_CONSUMER_SECRET
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_APPLICATION_ID
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_APPLICATION_SECRET_KEY
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_friends', 'public_profile']
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'  # TODO to avoid missing
# registration/login.html error
# need custom login view probably

# sandbox keys
PUBNUB_PUBLISH_KEY = 'pub-c-c852ffa1-72fc-41ed-9720-2f88b0e54880'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-e8bd5ce2-8506-11e2-ac19-12313f022c90'
PUBNUB_SECRET_KEY = 'sec-c-ZmE0OTc5MDYtYWUxNi00YTJjLWFjOGMtODVhNGQ5Y2JmNTdj'
PUBNUB_IS_SSL = False


DATABASES = {
    'default': dj_database_url.parse('postgres://postgres:postgres@' + \
                                     os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ':' + \
                                     os.environ['POSTGRES_PORT_5432_TCP_PORT'] + '/' + 'politikon')
}

# disabling SSL on local
SSLIFY_DISABLE = True

STATIC_URL = '/static/'
