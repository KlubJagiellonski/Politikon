from social.pipeline.partial import partial

import logging
logger = logging.getLogger(__name__)


@partial
def save_profile(backend, user, response, *args, **kwargs):
    print 'test2'
    logger(backend)
    logger(user)
    logger(response)

    if backend.name == 'facebook':
        print backend
    if backend.name == 'twitter':
        print backend
