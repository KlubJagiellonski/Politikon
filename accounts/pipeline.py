from social.pipeline.partial import partial

import logging
logger = logging.getLogger(__name__)


@partial
def save_profile(strategy, details, user=None, is_new=False, *args, **kwargs):
    logger(strategy)
    logger(details)
    logger(user)

    if strategy.name == 'facebook':
        print strategy
    if strategy.name == 'twitter':
        print strategy
