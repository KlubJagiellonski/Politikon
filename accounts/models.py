# coding: utf-8
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import logging
import os

from django.contrib.auth.models import AbstractBaseUser
from django.db import models, transaction
from django.db.models import F, Q
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from .managers import UserProfileManager
from bladepolska.snapshots import SnapshotAddon
from events.models import Bet, Event
from politikon.templatetags.format import formatted
from politikon.settings import STATIC_URL


logger = logging.getLogger(__name__)


def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('avatars', str(instance.username)+'.'+ext)


class UserProfile(AbstractBaseUser):
    class Meta:
        verbose_name = u'użytkownik'
        verbose_name_plural = u'użytkownicy'

    objects = UserProfileManager()
    # przeliczane rankingi: ranking, miesiąc, tydzień
    snapshots = SnapshotAddon(fields=[
        'total_cash',
        'total_given_cash',
        'portfolio_value'
    ])

    username = models.CharField(u"username", max_length=100, unique=True)
    email = models.CharField(u"email", max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    name = models.CharField(max_length=100, blank=True)
    is_admin = models.BooleanField(u"is an administrator", default=False)
    is_deleted = models.BooleanField(u"is deleted", default=False)

    is_staff = models.BooleanField(u"is staff", default=False)
    is_active = models.BooleanField(u"is active", default=False)

    is_vip = models.BooleanField(u"VIP", default=False)

    reset_date = models.DateTimeField(u"data ostatniej aktywacji", auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(null=True, blank=True)

    # TODO: czy to potrzebne?
    # Every new network relations also has to have 'related_name="django_user"'
    #     facebook_user = models.OneToOneField(FacebookUser, null=True,
    #     related_name="django_user", on_delete=models.SET_NULL)

    friends = models.ManyToManyField('self', related_name='friend_of')

    total_cash = models.IntegerField(u"ilość gotówki", default=0.)
    total_given_cash = models.IntegerField(u"ilość przyznanej gotówki w historii", default=0.)
    reputation = models.DecimalField(u"reputation", default=100, max_digits=12, decimal_places=2,
                                     null=True)
    portfolio_value = models.IntegerField(u"wartość portfela", default=0.)
    weekly_result = models.IntegerField(u"wynik tygodniowy", null=True, blank=True)
    monthly_result = models.IntegerField(u"wynik miesięczny", null=True, blank=True)

    web_site = models.URLField(u"strona www", max_length=255, default='')
    description = models.CharField(u"krótki opis", max_length=255, default='')
    facebook_user_id = models.BigIntegerField(u"facebook ID", default=None, blank=True, null=True)
    facebook_user = models.CharField(u"facebook URL", max_length=255, default=None, blank=True,
                                     null=True)
    twitter_user_id = models.BigIntegerField(u"twitter ID", default=None, blank=True, null=True)
    twitter_user = models.CharField(u"twitter URL", max_length=255, default=None, blank=True,
                                    null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    FACEBOOK_URL = 'https://www.facebook.com/{0}'
    TWITTER_URL = 'https://twitter.com/{0}'

    def __unicode__(self):
        return "%s" % self.username

    def save(self, **kwargs):
        """
        Calculate reputation
        :param kwargs:
        """
        if self.pk:
            self.calculate_reputation()

        super(UserProfile, self).save(**kwargs)

    # TODO what is this?
    #  @transaction.atomic
    #  def synchronize_facebook_friends(self):
        #  # Get friends
        #  facebook_friends_ids = self.facebook_user.friends_using_our_app
        #  if facebook_friends_ids is None:
            #  return

        #  django_friends_ids = FacebookUser.objects.django_users_for_ids(facebook_friends_ids).\
            #  values_list('id', flat=True)
        #  django_friends_ids_set = set(django_friends_ids)

        #  friends_through_model = self.friends.through
        #  friends_manager = friends_through_model.objects

        #  # Get current relations
        #  current_friends_ids_set = self.friends_ids_set

        #  # Add new
        #  new_friends_ids = list(django_friends_ids_set -
                               #  current_friends_ids_set)
        #  logger.debug("'User::synchronize_facebook_friends' adding %d new friends." % \
            #  len(new_friends_ids))

        #  if new_friends_ids:
            #  new_friends_through = [friends_through_model(from_user=self,
                                                         #  to_user_id=friend_id)
                                   #  for friend_id in new_friends_ids]
            #  friends_manager.bulk_create(new_friends_through)

        #  # Remove stale
        #  stale_friends_ids = list(current_friends_ids_set - django_friends_ids_set)
        #  logger.debug("'User::synchronize_facebook_friends' removing %d stale friends." % \
            #  len(stale_friends_ids))

        #  if stale_friends_ids:
            #  first_way_qs = Q(from_user=self, to_user__in=stale_friends_ids)
            #  second_way_qs = Q(to_user=self, from_user__in=stale_friends_ids)
            #  friends_manager.filter(first_way_qs | second_way_qs).delete()

    @property
    def statistics_dict(self):
        if self.reputation:
            reputation = "%s%%" % formatted(self.reputation)
        else:
            reputation = None
        return {
            'user_id': self.id,
            'total_cash': formatted(self.total_cash),
            'portfolio_value': formatted(self.portfolio_value),
            'reputation': reputation
        }

    # TODO what is this?
    #  @property
    #  def friends_ids_set(self):
        #  friends_through_model = self.friends.through
        #  friends_manager = friends_through_model.objects

        #  current_friends_ids = friends_manager.filter(Q(from_user=self) | Q(to_user=self)).\
            #  values_list('from_user_id', 'to_user_id')

        #  current_friends_ids_set = set()
        #  for from_id, to_id in current_friends_ids:
            #  if from_id != self.id:
                #  current_friends_ids_set.add(from_id)
            #  if to_id != self.id:
                #  current_friends_ids_set.add(to_id)

        #  return current_friends_ids_set

    def get_full_name(self):
        return "%s (%s)" % (self.name, self.username)

    @property
    def full_name(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def current_portfolio_value(self):
        """
        Calculate current portfolio_value, it is changing on event price change
        :return: portfolio value
        :rtype: int
        """
        portfolio_value = 0
        user_bets = Bet.objects.select_related('event').\
            filter(user=self, event__outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS, has__gt=0,
                   event__created_date__gt=self.reset_date)

        for bet in user_bets.iterator():
            price_field = "current_sell_for_price"
            if bet.outcome is False:
                price_field = "current_sell_against_price"

            portfolio_value += bet.has * getattr(bet.event, price_field)

        return portfolio_value

    def calculate_reputation(self):
        """
        Calculate and set user reputation
        """
        self.reputation = self.reputation_formula(self.portfolio_value,
                                                  self.total_cash, self.total_given_cash)

    @classmethod
    def reputation_formula(cls, portfolio_value, total_cash, total_given_cash):
        """
        Calculate and return reputation
        :param portfolio_value: total in wallet
        :type portfolio_value: int
        :param total_cash: unused reputation value
        :type total_cash: int
        :param total_given_cash: total reputation assigned for user
        :type total_given_cash: int
        :return: reputation value
        :rtype: Decimal
        """
        if total_given_cash == 0:
            return None
        else:
            return Decimal(portfolio_value + total_cash) / Decimal(total_given_cash) * 100

    #  @property
    #  def profile_photo(self):
        #  if self.facebook_user:
            #  return self.facebook_user.profile_photo

    def topup_cash(self, amount):
        self.total_cash += amount
        self.total_given_cash += amount

        from events.models import Transaction

        Transaction.objects.create(
            user=self,
            type=Transaction.TRANSACTION_TYPE_CHOICES.TOPPED_UP_BY_APP,
            quantity=1,
            price=amount
        )

        # from canvas.models import ActivityLog
        # ActivityLog.objects.register_transaction_activity(self, transaction)

        self.save()

    @property
    def is_superuser(self):
        return self.is_admin

    def get_absolute_url(self):
        """
        Get this user url

        :return: user url
        :rtype: str
        """
        return reverse('accounts:user', kwargs={'pk': str(self.pk)})

    def get_avatar_url(self):
        """
        Get this user avatar url

        :return: avatar url
        :rtype: str
        """
        if self.avatar:
            return self.avatar.url
        else:
            return STATIC_URL + "img/blank-avatar.jpg"

    def get_twitter_url(self):
        """
        Get this user twitter url: https://twitter.com/user

        :return: twitter user url
        :rtype: str
        """
        if self.twitter_user:
            return self.TWITTER_URL.format(self.twitter_user)
        return None

    def get_facebook_url(self):
        """
        Get this user facebook url: https://www.facebook.com/user

        :return: facebook user url
        :rtype: str
        """
        if self.facebook_user:
            return self.FACEBOOK_URL.format(self.facebook_user)
        return None

    def get_twitter_disconnect_url(self):
        """
        Url to disconnect user account from his Twitter account

        :return: Twitter disconnection url
        :rtype: str
        """
        # TODO: return that url

    def get_facebook_disconnect_url(self):
        """
        Url to disconnect user account from his Twitter account

        :return: Twitter disconnection url
        :rtype: str
        """
        # TODO: return that url

    def get_newest_results(self):
        """
        Get finished events and not seen by user
        :return: Bets list
        :rtype: QuerySet[Bet]
        """
        events_finished = (
            Event.EVENT_OUTCOME_CHOICES.CANCELLED,
            Event.EVENT_OUTCOME_CHOICES.FINISHED_YES,
            Event.EVENT_OUTCOME_CHOICES.FINISHED_NO,
        )
        return self.bets.filter(
            event__outcome__in=events_finished,
            is_new_resolved=True,
            has__gt=0,
        ).order_by('-event__end_date')

    def get_reputation_history(self):
        """
        Get historical data for user reputation (7 days)
        :return: chart points: dates and reputation
        :rtype: {int, [], []}
        """
        start_date = self.reset_date if self.reset_date > now() - timedelta(days=7) else now() - timedelta(days=7)
        snapshots = self.snapshots.filter(
            snapshot_of_id=self.id,
            created_at__gte=start_date,
        ).order_by('created_at')

        labels = []
        points = []
        old_created_at = ''
        for snapshot in snapshots:
            if old_created_at != snapshot.created_at.strftime('%m%d'):
                labels.append(u'{0} {1}'.format(
                    snapshot.created_at.day,
                    _(snapshot.created_at.strftime('%B'))
                ))
                reputation = self.reputation_formula(snapshot.portfolio_value, snapshot.total_cash,
                                                     snapshot.total_given_cash)
                points.append(str(int(reputation)))
            old_created_at = snapshot.created_at.strftime('%m%d')

        return {
            'id': self.id,
            'labels': labels,
            'points': points
        }

    def get_reputation_change(self, date):
        """
        Get change of reputation since date
        :return: change of reputation
        :rtype: int
        """
        start_date = self.reset_date if self.reset_date > date else date
        snapshots = self.snapshots.filter(
            snapshot_of_id=self.id,
            created_at__gte=date,
        ).order_by('created_at')
        if len(snapshots):
            old_reputation = self.reputation_formula(snapshots[0].portfolio_value,
                                                     snapshots[0].total_cash,
                                                     snapshots[0].total_given_cash)
            return int(self.reputation - old_reputation)
        else:
            return int(self.reputation) - 100

    def get_last_week_reputation_change(self):
        """
        Get change of reputation since last week
        :return: change of reputation
        :rtype: int
        """
        return self.get_reputation_change(now()-timedelta(days=7))

    def get_last_month_reputation_change(self):
        """
        Get change of reputation since last week
        :return: change of reputation
        :rtype: int
        """
        return self.get_reputation_change(now()-relativedelta(months=1))
