from bladepolska.redis_connection import RedisConnection
from constance import config
from django.db import transaction

from functools import partial
import datetime

import logging
logger = logging.getLogger(__name__)


USER_SYNC_QUEUE_KEY = "fb:tasks:usersync"
USER_FRIENDS_SYNC_QUEUE_KEY = "fb:tasks:userfriendssync"

PUBLISH_ACTIVITY_QUEUE_KEY = "fb:tasks:activities"


def add_facebook_user_sync_task(facebook_id):
    logger.debug("'fb:tasks:usersync' job added for user <%s>" % unicode(facebook_id))
    with RedisConnection as redis:
        redis.sadd(USER_SYNC_QUEUE_KEY, facebook_id)


def add_facebook_user_friends_sync_task(facebook_id):
    logger.debug("'fb:tasks:userfriendssync' job added for user <%s>" % unicode(facebook_id))
    with RedisConnection as redis:
        redis.sadd(USER_FRIENDS_SYNC_QUEUE_KEY, facebook_id)


def add_publish_activity_task(kwargs):
    logger.debug("'fb:tasks:activities' job added for kwargs <%s>" % unicode(kwargs))
    from .models import ActivityLog
    activity = ActivityLog(**kwargs)
    activity.save(force_insert=True)


def consume_facebook_user_sync_task():
    logger.debug("'fb:tasks:usersync' worker up")
    from .models import FacebookUser
    with RedisConnection as redis:
        for facebook_id in iter(partial(redis.spop, USER_SYNC_QUEUE_KEY), None):
            logger.debug("'fb:tasks:usersync' consuming job <%s>" % unicode(facebook_id))
            facebook_users = FacebookUser.objects.select_related('django_user').filter(facebook_id=facebook_id)

            for facebook_user in facebook_users:
                logger.debug("'fb:tasks:usersync' synchronizing user <%s>" % unicode(facebook_user))
                facebook_user.synchronize()
                logger.debug("'fb:tasks:usersync' synchronized user <%s>" % unicode(facebook_user))


def consume_facebook_user_friends_sync_task():
    logger.debug("'fb:tasks:userfriendssync' worker up")
    from django.contrib.auth import get_user_model
    with RedisConnection as redis:
        for facebook_id in iter(partial(redis.spop, USER_FRIENDS_SYNC_QUEUE_KEY), None):
            logger.debug("'fb:tasks:userfriendssync' consuming job <%s>" % unicode(facebook_id))
            django_users = get_user_model().objects.select_related('facebook_user').filter(facebook_user__facebook_id=facebook_id)
            for django_user in django_users:
                logger.debug("'fb:tasks:userfriendssync' synchronizing friends of user <%s>" % unicode(django_user))
                django_user.synchronize_facebook_friends()
                logger.debug("'fb:tasks:userfriendssync' synchronized friends of user <%s>" % unicode(django_user))


@transaction.commit_on_success()
def consume_publish_activities_tasks():
    logger.debug("'fb:tasks:activities' worker up")
    earlier_than = datetime.datetime.now() - datetime.timedelta(minutes=config.PUBLISH_DELAY_IN_MINUTES)

    from .models import ActivityLog
    activities_to_publish = ActivityLog.objects \
                                .select_for_update() \
                                .select_related('user', 'user__facebook_user', 'event') \
                                .filter(published=False, created_at__lt=earlier_than)

    for activity in activities_to_publish:
        logger.debug("'fb:tasks:activities' publishing job <%s>" % unicode(activity))
        activity.publish()
        logger.debug("'fb:tasks:activities' published job <%s>" % unicode(activity))
