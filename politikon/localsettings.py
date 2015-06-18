import os
from path import path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

DJANGO_PROJECT_ROOT = path(__file__).abspath().dirname().dirname()

MEDIA_ROOT = DJANGO_PROJECT_ROOT / 'static' / 'uploads'
MEDIA_URL = '/static/uploads/'

ALLOWED_HOSTS = ['localhost', 'http://politikon.dokku.me/', '192.168.59.103']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVE_STATIC_FILES = True
CELERY_ALWAYS_EAGER = True

FACEBOOK_APPLICATION_ID = "134939156680151"
FACEBOOK_APPLICATION_SECRET_KEY = "ce45e3ce267cd64a5cfee9743fc28d59"
FACEBOOK_APPLICATION_NAMESPACE = "politikon_staging"

FACEBOOK_REALTIME_VERIFY_TOKEN = "jkwjknvkjfwelnvljknsknv"

# social_auth configuration
SOCIAL_AUTH_TWITTER_KEY = '07cM50zfHeEZg2uuN0lkyyC4w'
SOCIAL_AUTH_TWITTER_SECRET = 'NQE2HRp135fn4rQSxvdMdcZ4Ug3HzG8wwhoKGGUjtxbFVk8Id4'
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_APPLICATION_ID
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_APPLICATION_SECRET_KEY
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
GOOGLE_OAUTH2_CLIENT_ID = '579638841369-9c8cliqj8o73nbufdbvfc144pqt81uc9.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'vUbknd9cRgqEIu4yZlgk4Yo9'

PUBNUB_PUBLISH_KEY = 'pub-c-99d402d4-9ece-4f63-a7ba-6c3ec61d36b4'
PUBNUB_SUBSCRIBE_KEY = 'sub-c-ba289054-825e-11e2-9881-12313f022c90'
PUBNUB_SECRET_KEY = 'sec-c-M2NiZjBjMWYtMWIyNC00MjIyLWJhYjAtNGZhY2IxNDQxZmEx'

DATABASE_URL = 'postgres://postgres:postgres@' + os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ':' + os.environ['POSTGRES_PORT_5432_TCP_PORT']  + '/' + 'politikon'

#disabling SSL on local
SSLIFY_DISABLE = True

SOUTH_MIGRATION_MODULES = {
    'default': 'social.apps.django_app.default.south_migrations',
}