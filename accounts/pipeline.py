from social.pipeline.partial import partial

import logging
logger = logging.getLogger(__name__)


@partial
def save_profile(strategy, details, user=None, is_new=False, *args, **kwargs):
    print(strategy)
    print(details)
    print(user)
