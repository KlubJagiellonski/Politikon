from django.conf import settings

from vendor import Pubnub as pubnub_api
from threading import local


class _PubNub(object):
    def __init__(self):
        self.local_storage = local()

    def __call__(self):
        if not hasattr(self.local_storage, 'Pubnub'):
            pubnub_args = (
                settings.PUBNUB_PUBLISH_KEY,
                settings.PUBNUB_SUBSCRIBE_KEY,
                settings.PUBNUB_SECRET_KEY,
                settings.PUBNUB_IS_SSL,
            )
            self.local_storage.Pubnub = pubnub_api.Pubnub(*pubnub_args)

        return self.local_storage.Pubnub

PubNub = _PubNub()
