import dj_database_url
from .base import *


DEBUG = False

SITE_ID = 2

ALLOWED_HOSTS = [
    'www.politikon.org.pl',
    'politikon.org.pl',
    'politikon.herokuapp.com',
    'politikon-staging.herokuapp.com',
    'politikon-lt.herokuapp.com',
]
CATCHALL_REDIRECT_HOSTNAME = os.environ.get("CATCHALL_REDIRECT_HOSTNAME")

DATABASES = {'default': dj_database_url.config()}

FACEBOOK_APPLICATION_ID = os.environ.get("FACEBOOK_APPLICATION_ID")
FACEBOOK_APPLICATION_SECRET_KEY = os.environ.get("FACEBOOK_APPLICATION_SECRET_KEY")
FACEBOOK_APPLICATION_NAMESPACE = os.environ.get("FACEBOOK_APPLICATION_NAMESPACE")
FACEBOOK_APPLICATION_MODERATORS = os.environ.get("FACEBOOK_APPLICATION_MODERATORS")

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")

# oauth-tokens settings
# # to keep in DB expired access tokens
OAUTH_TOKENS_HISTORY = True
OAUTH_TOKENS_TWITTER_CLIENT_ID = TWITTER_CONSUMER_KEY
OAUTH_TOKENS_TWITTER_CLIENT_SECRET = TWITTER_CONSUMER_SECRET
# user login
OAUTH_TOKENS_TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
# user password
OAUTH_TOKENS_TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

SOCIAL_AUTH_TWITTER_KEY = TWITTER_CONSUMER_KEY
SOCIAL_AUTH_TWITTER_SECRET = TWITTER_CONSUMER_SECRET
SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_APPLICATION_ID
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_APPLICATION_SECRET_KEY
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_friends', 'public_profile']
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'  # TODO to avoid missing
# registration/login.html error

PUBNUB_PUBLISH_KEY = os.environ.get("PUBNUB_PUBLISH_KEY")
PUBNUB_SUBSCRIBE_KEY = os.environ.get("PUBNUB_SUBSCRIBE_KEY")
PUBNUB_SECRET_KEY = os.environ.get("PUBNUB_SECRET_KEY")
PUBNUB_IS_SSL = False

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').\
    replace(',', ';')
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
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', '')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', '')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', 587)
EMAIL_USE_TLS = True
DEFAULT_EMAIL_FROM = 'Politikon <' + EMAIL_HOST_USER + '>'
EMAIL_DEFAULT_RECIPIENT = 'politikon.org.pl@gmail.com'

SERVE_STATIC_FILES = True

BASICAUTH = True
BASICAUTH_USERNAME = os.environ.get('BASICAUTH_USERNAME')
BASICAUTH_PASSWORD = os.environ.get('BASICAUTH_PASSWORD')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'politik')

AWS_S3_HOST = os.environ.get('AWS_S3_HOST', 's3.amazonaws.com')
AWS_S3_URL_PROTOCOL = 'https:'
AWS_QUERYSTRING_AUTH = False

ASSETS_AUTO_BUILD = False

from urlparse import urlparse
ES_URL = urlparse(os.environ.get('BONSAI_URL') or 'http://127.0.0.1:9200/')
ELASTIC_KEY = os.environ.get('ELASTIC_KEY', 'elastic')
ELASTIC_SECRET = os.environ.get('ELASTIC_SECRET', 'changeme')

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 12
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': ES_URL.scheme + '://' + ES_URL.hostname + ':443',
        'INDEX_NAME': 'haystack',
    },
}

if ES_URL.username:
    HAYSTACK_CONNECTIONS['default']['KWARGS'] = {"http_auth": ES_URL.username + ':' + ES_URL.password}

# uncomment when certificate renewing
# SSLIFY_DISABLE = True
