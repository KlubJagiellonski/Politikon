from django.db import models
from django.utils.translation import ugettext as _

from facepy import SignedRequest, GraphAPI
from fandjango.models import OAuthToken, User as OriginalFacebookUser

import datetime


class FacebookUserManager(models.Manager):
    def django_users_for_ids(self, ids):
        qs = self.select_related('django_user').filter(facebook_id__in=ids)

        return [row.django_user for row in qs if row.django_user]


class FacebookUser(models.Model):
    objects = FacebookUserManager()

    facebook_id = models.BigIntegerField(_('facebook id'), unique=True)
    facebook_username = models.CharField(_('facebook username'), max_length=255, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    middle_name = models.CharField(_('middle name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    authorized = models.BooleanField(_('authorized'), default=True)
    oauth_token = models.OneToOneField(OAuthToken, verbose_name=_('OAuth token'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    last_seen_at = models.DateTimeField(_('last seen at'), auto_now_add=True)

    profile_photo = models.TextField(blank=True, null=True)

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

    @property
    def all_friends_ids(self):
        friends_ids = []

        friends_reply_generator = self.graph.get('me/friends', page=True)
        for friends_reply in friends_reply_generator:
            friends_ids += [friend.get('id') for friend in friends_reply.get('data', [])]

        return filter(lambda u: u is not None, friends_ids)

#   Every new network user model also has to have friends_using_our_app property
    @property
    def friends_using_our_app(self):
        friends_ids = self.all_friends_ids

        return self.__class__.objects.filter(facebook_id__in=friends_ids)

    def synchronize(self):
        fetched_fields = [
            'id', 'name',
            'username', 'first_name', 'middle_name', 'last_name',
            'picture'
        ]
        path = 'me?fields=%s' % ','.join(fetched_fields)
        profile = self.graph.get(path)

        self.facebook_username = profile.get('username')
        self.first_name = profile.get('first_name')
        self.middle_name = profile.get('middle_name')
        self.last_name = profile.get('last_name')

        try:
            self.birthday = datetime.strptime(profile['birthday'], '%m/%d/%Y') if profile.has_key('birthday') else None
        except:
            self.birthday = None

        self.profile_photo = profile.get('picture', {}).get('data', {}).get('url', None)

        self.save()

ACTIVITIES = {
    1: 'NEW_USER',
    2: 'NEW_USER',
    3: 'NEW_USER',
    4: 'NEW_USER',
    5: 'NEW_USER',
}


class ActivityLogManager(models.Manager):
    pass


class ActivityLog(models.Model):
    objects = ActivityLogManager()
    