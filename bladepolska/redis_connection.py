from django.conf import settings
from django.core import signals

import redis
from threading import local

class _RedisConnection(object):
    def __init__(self, db=0):
        self.connection = local()
        self.db = getattr(settings, 'REDIS_DB', 0)
 
    def connect(self):
        if hasattr(settings, 'REDIS_BASE_URL') and settings.REDIS_BASE_URL is not None:
            self.connection.r = redis.from_url(settings.REDIS_BASE_URL)
        else:
            if hasattr(settings, 'REDIS_PATH'):
                self.connection.r = redis.StrictRedis(unix_socket_path=getattr(settings, 'REDIS_PATH'), db=self.db)
            else:
                self.connection.r = redis.StrictRedis(host=getattr(settings, 'REDIS_HOST', 'localhost'), port=getattr(settings, 'REDIS_PORT', 6379), password=getattr(settings, 'REDIS_PASSWORD', None), db=self.db)

    def is_connected(self):
        return hasattr(self.connection, 'r')

    def disconnect(self, **kwargs):
        if self.is_connected():
            self.connection.r.connection_pool.disconnect()

    def redis(self):
        if not self.is_connected():
            self.connect()
        return self.connection.r

    def __enter__(self):
        if not self.is_connected():
            self.connect()
        return self.connection.r

    def __exit__(self, type, value, traceback):
        pass

RedisConnection = _RedisConnection()

signals.request_finished.connect(RedisConnection.disconnect)
