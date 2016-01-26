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
    url = u'https://graph.facebook.com/{0}/' \
          u'friends' \
          u'&access_token={1}'.format(
              uid,
              response['access_token']
          )
    print "RESPONSE",response['access_token']
    request = urllib2.Request(url)
    print("URL",url)
    print(request)
    count = json.loads(urllib2.urlopen(request).read()).get('summary').get('total_count')
