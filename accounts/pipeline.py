from social.pipeline.partial import partial

import logging
logger = logging.getLogger(__name__)
from constance import  config
import urllib2
from requests import request, HTTPError

from django.core.files.base import ContentFile

@partial
def save_profile(strategy, user, response, details,
                         is_new=False,*args,**kwargs):
    # print(is_new)
    # print(strategy)
    # print(details)
    # uid = kwargs['uid']
    backend = kwargs['backend']

    if is_new and backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            user.avatar.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))

        playing_friends_count = len(response['friends']['data'])
        if playing_friends_count < config.REQUIRED_FRIENDS_THRESHOLD:
            user.is_active = False
        else:
            user.is_active = True

        user.save()

