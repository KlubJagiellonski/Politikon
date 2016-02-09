from social.pipeline.partial import partial

import logging
logger = logging.getLogger(__name__)
import urllib2
import json


@partial
def save_profile(*args, **kwargs):
    # print(is_new)
    # print(strategy)
    # print(details)
    response = kwargs['response']
    uid = kwargs['uid']
    friend_count = response['friends']['summary']['total_count']
    print(friend_count)
