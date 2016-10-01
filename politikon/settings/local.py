# local machine settings overriding the devsettings.
# Idealy this file should be empty
from .dev import *


MEDIA_URL = 'http://local.politikon.org.pl:8000/static/uploads/'

SITE_URL = 'http://local.politikon.org.pl:8000/'

REDIS_BASE_URL = os.environ.get('REDISTOGO_URL', 'redis://172.17.0.4:6379')
REDIS_PARAMS = urlparse.urlparse(REDIS_BASE_URL)

# Celery config

REDIS_HOST = REDIS_PARAMS.hostname
REDIS_PORT = REDIS_PARAMS.port
REDIS_DB = 0
REDIS_CONNECT_RETRY = True

BROKER_URL = REDIS_BASE_URL + "/0"
CELERY_RESULT_BACKEND = REDIS_BASE_URL + "/1"
