# coding: utf-8

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

from facepy import SignedRequest, GraphAPI
from facepy.exceptions import OAuthError
from fandjango.models import OAuthToken, User as OriginalFacebookUser

import datetime

from events.models import Event, TRANSACTION_TYPES_INV_DICT
from . import tasks

import logging
logger = logging.getLogger(__name__)


class FacebookUserManager(models.Manager):
    def django_users_for_ids(self, ids):
        return get_user_model().objects.filter(facebook_user__in=ids)


class FacebookUser(models.Model):
    objects = FacebookUserManager()

    facebook_id = models.BigIntegerField(_('facebook id'), unique=True)
    facebook_username = models.CharField(_('facebook username'), max_length=255, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    middle_name = models.CharField(_('middle name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    authorized = models.BooleanField(_('authorized'), default=True)
    oauth_token = models.OneToOneField(OAuthToken, verbose_name=_('OAuth token'), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    last_seen_at = models.DateTimeField(_('last seen at'), auto_now_add=True)

    profile_photo = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.facebook_id

    @property
    def full_name(self):
        """Return the user's first name."""
        if self.first_name and self.middle_name and self.last_name:
            return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)

    @property
    def graph(self):
        return GraphAPI(self.oauth_token.token)

    def fb_get(self, url, noncritical=True, **kwargs):
        try:
            return self.graph.get(url, **kwargs)
        except OAuthError as e:
            if not noncritical:
                raise

            if e.code == 190:
                # Stale oauth_token.
                self.oauth_token.delete()
                self.oauth_token = None
                self.save(update_fields=['oauth_token'])

            logger.exception("FacebookUser(#%(id)d)::fb_get() failed with OAuthError, will not retry." % {
                'id': self.id,
            })
        except:
            raise

    def fb_post(self, url, payload={}, noncritical=True):
        try:
            return self.graph.post(path=url, retry=0, **payload)
        except OAuthError as e:
            if not noncritical:
                raise

            if e.code == 190:
                # Stale oauth_token.
                self.oauth_token.delete()
                self.oauth_token = None
                self.save(update_fields=['oauth_token'])

            logger.exception("FacebookUser(#%(id)d)::fb_get() failed with OAuthError, will not retry." % {
                'id': self.id,
            })
        except:
            raise


    @property
    def all_friends_ids(self):
        friends_ids = []

        friends_reply_generator = self.fb_get('me/friends', page=True)
        if friends_reply_generator is None:
            return None

        for friends_reply in friends_reply_generator:
            friends_ids += [friend.get('id') for friend in friends_reply.get('data', [])]

        return filter(lambda u: u is not None, friends_ids)

#   Every new network user model also has to have friends_using_our_app property
    @property
    def friends_using_our_app(self):
        friends_ids = self.all_friends_ids
        if friends_ids is None:
            return None
        if friends_ids == []:
            return []

        return self.__class__.objects.filter(facebook_id__in=friends_ids)

    def synchronize(self, commit=True):
        logger.debug("FacebookUser(%s).synchronize(%d)" % (self, commit))

        fetched_fields = [
            'id', 'name',
            'username', 'first_name', 'middle_name', 'last_name',
            'picture'
        ]
        path = 'me?fields=%s' % ','.join(fetched_fields)
        profile = self.fb_get(path)

        if profile:
            self.facebook_username = profile.get('username')
            self.first_name = profile.get('first_name')
            self.middle_name = profile.get('middle_name')
            self.last_name = profile.get('last_name')

            try:
                self.birthday = datetime.strptime(profile['birthday'], '%m/%d/%Y') if profile.has_key('birthday') else None
            except:
                self.birthday = None

            self.profile_photo = profile.get('picture', {}).get('data', {}).get('url', None)

        if commit:
            self.save()

ACTIVITIES_DICT = {
    'NEW_USER': 1,
    'BOUGHT_YES': 2,
    'BOUGHT_NO': 3,
    'SOLD_YES': 4,
    'SOLD_NO': 5,
    'WON_BET': 6,
    'LOST_BET': 7,
    'GOT_CASH': 8
}

ACTIVITIES = (
    (1, u'nowy użytkownik'),
    (2, u'kupił zakład na TAK'),
    (3, u'kupił zakład na NIE'),
    (4, u'sprzedał zakład na TAK'),
    (5, u'sprzedał zakład na NIE'),
    (6, u'wygrał zakład'),
    (7, u'przegrał zakład')
)

TRANSACTION_TYPE_TO_ACTIVITY_MAP = {
    'BUY_YES': 'BOUGHT_YES',
    'SELL_YES': 'SOLD_YES',
    'BUY_NO': 'BOUGHT_NO',
    'SELL_NO': 'SOLD_NO',
    'EVENT_WON_PRIZE': 'WON_BET',
    'TOPPED_UP_BY_APP': 'GOT_CASH',
}


class ActivityLogManager(models.Manager):
    def register_new_user_activity(self, user):
        kwargs = {
            'activity_type': ACTIVITIES_DICT['NEW_USER'],
            'user_id': user.id
        }

        tasks.add_publish_activity_task(kwargs)

    def register_transaction_activity(self, user, transaction):
        transaction_type = TRANSACTION_TYPES_INV_DICT.get(transaction.type)
        activity_type = TRANSACTION_TYPE_TO_ACTIVITY_MAP.get(transaction_type)

        if not activity_type:
            logger.warning("'ActivityLogManager::register_transaction_activity' No known activity type for transaction type %s." % unicode(transaction.type))
            return

        kwargs = {
            'activity_type': ACTIVITIES_DICT[activity_type],
            'user_id': user.id,
            'event_id': transaction.event_id
        }

        tasks.add_publish_activity_task(kwargs)


class ActivityLog(models.Model):
    objects = ActivityLogManager()
    ACTIVITY_ASSUME_YES_ACTION = "assume_yes"
    ACTIVITY_ASSUME_NO_ACTION = "assume_no"

    activity_type = models.PositiveIntegerField(null=False, choices=ACTIVITIES, default=9999)
    event = models.ForeignKey(Event, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('created at'))

    def publish(self):
        if not self.user or not self.user.facebook_user:
            return

        facebook_user = self.user.facebook_user

        url, payload = "", {}

        if self.activity_type == ACTIVITIES_DICT['NEW_USER']:
            pass
        if self.activity_type == ACTIVITIES_DICT['BOUGHT_YES']:
            url = "/me/%(namespace)s:%(action)s" % {
                'namespace': settings.FACEBOOK_APPLICATION_NAMESPACE,
                'action': ActivityLog.ACTIVITY_ASSUME_YES_ACTION
            }

            payload = {
                'event': self.event.get_absolute_facebook_object_url()
            }

        if self.activity_type == ACTIVITIES_DICT['BOUGHT_NO']:
            url = "/me/%(namespace)s:%(action)s" % {
                'namespace': settings.FACEBOOK_APPLICATION_NAMESPACE,
                'action': ActivityLog.ACTIVITY_ASSUME_NO_ACTION
            }

            payload = {
                'event': self.event.get_absolute_facebook_object_url()
            }

        if self.activity_type == ACTIVITIES_DICT['SOLD_YES']:
            pass
        if self.activity_type == ACTIVITIES_DICT['SOLD_NO']:
            pass
        if self.activity_type == ACTIVITIES_DICT['WON_BET']:
            pass
        if self.activity_type == ACTIVITIES_DICT['LOST_BET']:
            pass
        if self.activity_type == ACTIVITIES_DICT['GOT_CASH']:
            pass

        if url:
            logger.debug('ActivityLog(#%(id)d)::publish() publishing %(url)s, with: %(payload)s for user <%(user)s>.' % {
                'id': self.id,
                'user': facebook_user,
                'url': url,
                'payload': payload
            })

            facebook_user.fb_post(url, payload)

        self.published = True
        self.save(force_update=True)
