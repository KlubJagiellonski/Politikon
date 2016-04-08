# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
import logging
from math import exp
from unidecode import unidecode
import pytz

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.template.defaultfilters import slugify
from django.utils.timezone import datetime

from .exceptions import UnknownOutcome
from .managers import EventManager, BetManager, TransactionManager
from bladepolska.snapshots import SnapshotAddon
from bladepolska.site import current_domain
from politikon.choices import Choices


logger = logging.getLogger(__name__)


_MONTHS = {
    1: 'Stycznia',
    2: 'Lutego',
    3: 'Marca',
    4: 'Kwietnia',
    5: 'Maja',
    6: 'Czerwca',
    7: 'Lipca',
    8: 'Sierpnia',
    9: 'Września',
    10: 'Października',
    11: 'Listopada',
    12: 'Grudnia'
}


class Event(models.Model):
    """
    Event model represents exactly real question which you can answer YES or NO.
    """

    EVENT_OUTCOME_CHOICES = Choices(
        ('IN_PROGRESS', 1, u'w trakcie'),
        ('CANCELLED', 2, u'anulowane'),
        ('FINISHED_YES', 3, u'rozstrzygnięte na TAK'),
        ('FINISHED_NO', 4, u'rozstrzygnięte na NIE'),
    )

    BOOLEAN_OUTCOME_DICT = {
        EVENT_OUTCOME_CHOICES.FINISHED_YES: True,
        EVENT_OUTCOME_CHOICES.FINISHED_NO: False
    }

    BEGIN_PRICE = 50
    DAYS_BEFORE_START = 3
    PRIZE_FOR_WINNING = 100

    objects = EventManager()
    snapshots = SnapshotAddon(fields=[
        'current_buy_for_price',
        'current_buy_against_price',
        'current_sell_for_price',
        'current_sell_against_price',
        'Q_for',
        'Q_against',
        'B'
    ])

    title = models.TextField(u'tytuł wydarzenia')
    short_title = models.TextField(u'tytuł promocyjny wydarzenia')

    title_fb_yes = models.TextField(u'tytuł na TAK obiektu FB')
    title_fb_no = models.TextField(u'tytuł na NIE obiektu FB')

    description = models.TextField(u'pełny opis wydarzenia', default='')

    small_image = models.\
        ImageField(u'mały obrazek 340x250', upload_to='events_small',
                   null=True)
    big_image = models.\
        ImageField(u'duży obrazek 1250x510', upload_to='events_big', null=True)

    is_featured = models.BooleanField(u'featured', default=False)
    is_front = models.BooleanField(u'front', default=False)
    outcome = models.\
        PositiveIntegerField(u'rozstrzygnięcie', choices=EVENT_OUTCOME_CHOICES,
                             default=1)
    outcome_reason = models.\
        TextField(u'uzazadnienie wyniku', default='', blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    estimated_end_date = models.\
        DateTimeField(u'przewidywana data rozstrzygnięcia')
    end_date = models.DateTimeField(u'data rozstrzygnięcia', null=True)

    current_buy_for_price = models.\
        IntegerField(u'cena nabycia akcji zdarzenia', default=BEGIN_PRICE)
    current_buy_against_price = models.\
        IntegerField(u'cena nabycia akcji zdarzenia przeciwnego', default=BEGIN_PRICE)
    current_sell_for_price = models.\
        IntegerField(u'cena sprzedaży akcji zdarzenia', default=BEGIN_PRICE)
    current_sell_against_price = models.\
        IntegerField(u'cena sprzedaży akcji zdarzenia przeciwnego',
                     default=BEGIN_PRICE)

    last_transaction_date = models.\
        DateTimeField(u'data ostatniej transakcji', null=True)

    Q_for = models.IntegerField(u'zakładów na TAK', default=0)
    Q_against = models.IntegerField(u'zakładów na NIE', default=0)
    turnover = models.IntegerField(u'obrót', default=0, db_index=True)

    absolute_price_change = models.\
        IntegerField(u'zmiana ceny (wartość absolutna)', db_index=True,
                     default=0)
    price_change = models.IntegerField(u'zmiana ceny', default=0)

    # constant for calculating event change
    B = models.FloatField(u'stała B', default=5)

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        """
        Recalculate prices for event and optionally change front event
        :param kwargs:
        """
        if not self.id:
            self.recalculate_prices()

        if self.is_front and self.is_in_progress:
            front_events = Event.objects.filter(is_front=True)
            for e in front_events:
                e.is_front = False
                e.save()

        super(Event, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={'pk': self.pk})

    def get_relative_url(self):
        return '/event/%(id)d-%(title)s' % {'id': self.id,
                                            'title': slugify(unidecode
                                                             (self.title))}

    def get_absolute_facebook_object_url(self):
        return 'http://%(domain)s%(url)s' % {
            'domain': current_domain(),
            'url': reverse('events:event_facebook_object_detail',
                           kwargs={'event_id': self.id})
        }

    @property
    def is_in_progress(self):
        return self.outcome == Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS

    @property
    def publish_channel(self):
        return 'event_%d' % self.id

    @property
    def event_dict(self):
        return {
            'event_id': self.id,
            'buy_for_price': self.current_buy_for_price,
            'buy_against_price': self.current_buy_against_price,
            'sell_for_price': self.current_sell_for_price,
            'sell_against_price': self.current_sell_against_price,
        }

    def price_for_outcome(self, outcome, direction='BUY'):
        if (direction, outcome) not in Bet.BET_OUTCOMES_TO_PRICE_ATTR:
            raise UnknownOutcome()

        attr = Bet.BET_OUTCOMES_TO_PRICE_ATTR[(direction, outcome)]
        return getattr(self, attr)

    @transaction.atomic
    def get_chart_points(self):
        """
        Get last transactions price for every day; days range is max 14
        :return: chart points
        :rtype: {int, [], []}
        """
        if self.end_date and self.end_date < datetime.now(tz=pytz.UTC):
            # for finished event last date point is end_date
            last_date = self.end_date
        else:
            # for event in progress last date point is yesterday
            last_date = datetime.now().replace\
                (hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)

        first_date = (last_date - relativedelta(weeks=2)).\
            replace(hour=0, minute=0, second=0, microsecond=0)

        # Default is start price: 50
        last_price = Event.BEGIN_PRICE
        step_date = first_date
        labels = []
        points = []

        if step_date < self.created_date - relativedelta\
                (days=Event.DAYS_BEFORE_START):
            step_date = self.created_date - relativedelta\
                (days=Event.DAYS_BEFORE_START)

        while self.created_date.replace\
                (hour=0, minute=0, second=0, microsecond=0,
                 tzinfo=pytz.UTC) > step_date:
            labels.append(str(step_date.day) + ' %s' % _MONTHS[step_date.month])
            step_date += relativedelta(days=1)
            points.append(Event.BEGIN_PRICE)

        while step_date < last_date:
            labels.append(str(step_date.day) + ' %s' % _MONTHS[step_date.month])
            step_date += relativedelta(days=1)
            ts = Transaction.objects.filter(event=self,
                                            date__lte=step_date,
                                            type__in=Transaction.BUY_SELL_TYPES,
                                            ).order_by('-date')[:1]
            if ts.exists():
                t = ts[0]
                if t.type == Transaction.TRANSACTION_TYPE_CHOICES.BUY_NO \
                        or t.type == Transaction.\
                        TRANSACTION_TYPE_CHOICES.SELL_NO:
                    last_price = 100 - abs(t.price)
                else:
                    last_price = abs(t.price)
            points.append(last_price)

        return {
            'id': self.id,
            'labels': labels,
            'points': points
        }

    def get_user_bet(self, user):
        """
        get bet summary for user; user maybe anonymous.
        """
        if user.pk:
            # TODO: resolve problem with bets > 1.   Which bet choose?
            # comment: mayby condition has__gt=0 resolve this problem.
            bets = self.bets.filter(user=user, has__gt=0).order_by('-id')
            if bets.exists():
                bet = bets[0]
                bet.extension = {
                    'is_user': True,
                    'has_any': True,
                    'buyYES': bet.outcome,
                    'buyNO': not bet.outcome,
                    'outcomeYES': "YES" if bet.outcome else "NO",
                    'outcomeNO': "YES" if bet.outcome else "NO",
                    'priceYES': self.current_buy_for_price if bet.outcome
                    else self.current_sell_against_price,
                    'priceNO': self.current_sell_for_price if bet.outcome
                    else self.current_buy_against_price,
                    'textYES': "+" if bet.outcome else "-",
                    'textNO': "-" if bet.outcome else "+",
                    'has': bet.has,
                    'classOutcome': "YES" if bet.outcome else "NO",
                    'textOutcome': "TAK" if bet.outcome else "NIE",
                    'avgPrice': bet.bought_avg_price,
                }
                return bet
            else:
                bet = Bet(event=self, user=user)
        else:
            bet = Bet(event=self)
        # this bet.extension is for users with no bets and for anonymous
        bet.extension = {
            'is_user': False,
            'has_any': False,
            'buyYES': True,
            'buyNO': True,
            'outcomeYES': "YES",
            'outcomeNO': "NO",
            'priceYES': self.current_buy_for_price,
            'priceNO': self.current_buy_against_price,
            'textYES': "TAK",
            'textNO': "NIE"
        }
        if user.pk:
            bet.extension['is_user'] = True
        return bet

    def get_bet_social(self):
        """
        Get users who bought this event
        :return: Dict with 4 keys: 2 QuerySet with YES users and NO users, 2
        integers with counts
        :rtype: dict{}
        """
        response = {}
        bet_social_yes = Bet.objects.filter(
                event=self,
                outcome=True,  # bought YES
                has__gt=0,
        )
        response['yes_count'] = bet_social_yes.count()
        response['yes_bets'] = bet_social_yes[:6]

        bet_social_no = Bet.objects.filter(
                event=self,
                outcome=False,  # bought NO
                has__gt=0,
        )
        response['no_count'] = bet_social_no.count()
        response['no_bets'] = bet_social_no[:6]
        return response

    def increment_quantity(self, outcome, by_amount):
        """
        Used when operation buy or sell occurs
        :param outcome: event outcome - YES or NO; True for YES
        :type outcome: bool
        :param by_amount: operations count, usually 1
        :type by_amount: int
        :return:
        """
        if outcome not in Bet.BET_OUTCOMES_TO_QUANTITY_ATTR:
            raise UnknownOutcome()

        attr = Bet.BET_OUTCOMES_TO_QUANTITY_ATTR[outcome]
        setattr(self, attr, getattr(self, attr) + by_amount)

        self.recalculate_prices()

    def increment_turnover(self, by_amount):
        """
        Turnover increases +1 when operation buy or sell occurs
        :param by_amount: operations count, usually 1
        :type by_amount: int
        """
        self.turnover += by_amount

    def recalculate_prices(self):
        """
        Calculate 4 prices for event
        """
        factor = 100.

        B = self.B

        Q_for = self.Q_for
        Q_against = self.Q_against
        Q_for_sell = max(0, Q_for - 1)
        Q_against_sell = max(0, Q_against - 1)

        e_for_buy = exp(Q_for / B)
        e_against_buy = exp(Q_against / B)
        e_for_sell = exp(Q_for_sell / B)
        e_against_sell = exp(Q_against_sell / B)

        buy_for_price = e_for_buy / float(e_for_buy + e_against_buy)
        buy_against_price = e_against_buy / float(e_for_buy + e_against_buy)
        sell_for_price = e_for_sell / float(e_for_sell + e_against_buy)
        sell_against_price = e_against_sell / float(e_for_buy + e_against_sell)

        self.current_buy_for_price = round(factor * buy_for_price, 0)
        self.current_buy_against_price = round(factor * buy_against_price, 0)
        self.current_sell_for_price = round(factor * sell_for_price, 0)
        self.current_sell_against_price = round(factor * sell_against_price, 0)

    @transaction.atomic
    def finish(self, outcome):
        """
        Set Event finish status
        :param outcome: outcome status; True if YES
        :type outcome: bool
        :return: True if event is finished
        :rtype: bool
        """
        if self.outcome != self.EVENT_OUTCOME_CHOICES.IN_PROGRESS:
            return False
        self.outcome = outcome
        self.end_date = datetime.now()
        self.save()
        return True

    @transaction.atomic
    def finish_with_outcome(self, outcome):
        """
        main finish status
        :param outcome: outcome status; True if YES
        :type outcome: bool
        :return: True if event is finished
        :rtype: bool
        """
        if not self.finish(outcome):
            return False
        for bet in Bet.objects.filter(event=self):
            if bet.outcome == self.BOOLEAN_OUTCOME_DICT[outcome]:
                bet.rewarded_total += self.PRIZE_FOR_WINNING * bet.has
                bet.user.total_cash += bet.rewarded_total
                bet.user.save()
                Transaction.objects.create(
                    user=bet.user,
                    event=self,
                    type=Transaction.TRANSACTION_TYPE_CHOICES.EVENT_WON_PRIZE,
                    quantity=bet.has,
                    price=self.PRIZE_FOR_WINNING
                )
            # This cause display event in "latest outcome"
            bet.is_new_resolved = True
            bet.save()
        return True

    @transaction.atomic
    def finish_yes(self):
        """
        if event is finished on YES then prizes calculate
        :return: True if event is finished
        :rtype: bool
        """
        return self.finish_with_outcome(self.EVENT_OUTCOME_CHOICES.
                                        FINISHED_YES)

    @transaction.atomic
    def finish_no(self):
        """
        if event is finished on NO then prizes calculate
        :return: True if event is finished
        :rtype: bool
        """
        return self.finish_with_outcome(self.EVENT_OUTCOME_CHOICES.
                                        FINISHED_NO)

    @transaction.atomic
    def cancel(self):
        """
        refund for users on cancel event.
        :return: True if event is finished
        :rtype: bool
        """
        if not self.finish(self.EVENT_OUTCOME_CHOICES.CANCELLED):
            return False
        users = {}
        for t in Transaction.objects.filter(event=self).order_by('user'):
            if t.user not in users:
                users.update({
                    t.user: 0
                })
            if t.type == t.TRANSACTION_TYPE_CHOICES.BUY_YES or \
                    t.type == t.TRANSACTION_TYPE_CHOICES.BUY_NO or \
                    t.type == t.TRANSACTION_TYPE_CHOICES.SELL_YES or \
                    t.type == t.TRANSACTION_TYPE_CHOICES.SELL_NO:
                # for transaction type BUY the price is below 0
                users[t.user] += t.quantity * t.price
        for user, refund in users.iteritems():
            if refund == 0:
                continue
            user.total_cash += refund
            user.save()
            if refund > 0:
                transaction_type = t.TRANSACTION_TYPE_CHOICES.\
                    EVENT_CANCELLED_REFUND
            else:
                transaction_type = t.TRANSACTION_TYPE_CHOICES.\
                    EVENT_CANCELLED_DEBIT
            Transaction.objects.create(
                user=user,
                event=self,
                type=transaction_type,
                price=abs(refund)
            )
        return True

    def get_related(self, user, number=9):
        """
        Get events related to this event
        :param user: logged user if exists
        :type user: UserProfile
        :param number: maximal events number
        :type number: int
        :return: list of related events
        :rtype:  QuerySet
        """
        relates = self.these_events.all().only('related')[:number]
        events = []
        for relation in relates:
            event = relation.related
            event.my_bet = event.get_user_bet(user)
            events.append(event)
        return events


class RelatedEvent(models.Model):
    """
    Relates between events. Relates are one side: one element in this model
    means that "related" event is on the list "Powiązane Wydarzenia" "event".
    Other side relation need another element.
    """
    event = models.ForeignKey(Event, null=True, related_name='these_events',
                              related_query_name='this_event')
    related = models.ForeignKey(Event, null=True, related_name='relates',
                                related_query_name='related')


class Bet(models.Model):
    """
    Created when user choose YES or NO for event.
    """

    BET_OUTCOME_CHOICES = Choices(
        ('YES', True, u'udziały na TAK'),
        ('NO', False, u'udziały na NIE'),
    )

    BET_OUTCOMES_TO_PRICE_ATTR = {
        ('BUY', 'YES'): 'current_buy_for_price',
        ('BUY', 'NO'): 'current_buy_against_price',
        ('SELL', 'YES'): 'current_sell_for_price',
        ('SELL', 'NO'): 'current_sell_against_price'
    }

    BET_OUTCOMES_TO_QUANTITY_ATTR = {
        'YES': 'Q_for',
        'NO': 'Q_against'
    }

    objects = BetManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False,
                             related_name='bets', related_query_name='bet')
    event = models.ForeignKey(Event, null=False, related_name='bets',
                              related_query_name='bet')
    outcome = models.BooleanField(u'zakład na TAK',
                                  choices=BET_OUTCOME_CHOICES)
    # most important param: how many bets user has.
    has = models.PositiveIntegerField(u'posiadane zakłady', default=0,
                                      null=False)
    bought = models.PositiveIntegerField(u'kupione zakłady', default=0,
                                         null=False)
    sold = models.PositiveIntegerField(u'sprzedane zakłady', default=0,
                                       null=False)
    bought_avg_price = models.FloatField(u'kupione po średniej cenie',
                                         default=0, null=False)
    sold_avg_price = models.FloatField(u'sprzedane po średniej cenie',
                                       default=0, null=False)
    rewarded_total = models.IntegerField(u'nagroda za wynik', default=0,
                                         null=False)
    # this is used to show event in my wallet.
    is_new_resolved = models.BooleanField(u'ostatnio rozstrzygnięte',
                                          default=False, null=False)

    @property
    def bet_dict(self):
        """
        Dictionary with bet values
        :return: bet vaules
        :rtype: {}
        """
        return {
            'bet_id': self.id,
            'event_id': self.event.id,
            'user_id': self.user.id,
            'outcome': self.outcome,
            'has': self.has,
            'bought': self.bought,
            'sold': self.sold,
            'bought_avg_price': self.bought_avg_price,
            'sold_avg_price': self.sold_avg_price,
            'rewarded_total': self.rewarded_total,
        }

    def __unicode__(self):
        return u'zakłady %s na %s' % (self.user, self.event)

    def current_event_price(self):
        """
        Get current price for event. Price depend on bet.outcome
        :return: current price
        :rtype: int
        """
        if self.outcome:
            return self.event.current_buy_for_price
        else:
            return self.event.current_buy_against_price

    def is_won(self):
        """
        winning bet when bet has outcome True  and event.outcome is 3
        (FINISHED_YES) or
        when bet has outcome False and event.outcome is 4 (FINISHED_NO)
        :return: True if won
        :rtype: bool
        """
        if self.outcome and self.event.outcome == Event.EVENT_OUTCOME_CHOICES.\
                FINISHED_YES:
            return True
        elif not self.outcome and self.event.outcome == Event.\
                EVENT_OUTCOME_CHOICES.FINISHED_NO:
            return True
        return False

    def get_wallet_change(self):
        """
        Get amount won or lose after event finished. For events in progress
        get amount possible to win.
        :return: more or less than zero
        :rtype: int
        """
        if self.is_won() or self.event.outcome == Event.EVENT_OUTCOME_CHOICES.\
                IN_PROGRESS:
            return self.get_won() - self.get_invested()
        else:
            return -self.get_invested()

    def get_invested(self):
        """
        How many invested in this bet
        :return: price above zero
        :rtype: float
        """
        if self.event.outcome == Event.EVENT_OUTCOME_CHOICES.CANCELLED:
            return 0
        return round(self.has * self.bought_avg_price, 0)

    def get_won(self):
        """
        Get amount won or possibility to win.
        :return: price
        :rtype: int
        """
        if self.is_won() or self.event.outcome == Event.EVENT_OUTCOME_CHOICES.\
                IN_PROGRESS:
            return self.has * Event.PRIZE_FOR_WINNING
        else:
            return 0

    def is_finished_yes(self):
        """
        Result for bet
        :return: True if event resolved for YES
        :rtype: bool
        """
        return self.event.outcome == Event.EVENT_OUTCOME_CHOICES.FINISHED_YES

    def is_finished_no(self):
        """
        Result for bet
        :return: True if event resolved for NO
        :rtype: bool
        """
        return self.event.outcome == Event.EVENT_OUTCOME_CHOICES.FINISHED_NO

    def is_cancelled(self):
        """
        Result for bet
        :return: True if canceled bet
        :rtype: bool
        """
        return self.event.outcome == Event.EVENT_OUTCOME_CHOICES.CANCELLED


class Transaction(models.Model):
    """
    Operation buy or sell or other for user and event
    """

    TRANSACTION_TYPE_CHOICES = Choices(
        ('BUY_YES', 1, u'zakup udziałów na TAK'),
        ('SELL_YES', 2, u'sprzedaż udziałów na TAK'),
        ('BUY_NO', 3, u'zakup udziałów na NIE'),
        ('SELL_NO', 4, u'sprzedaż udziałów na NIE'),
        ('EVENT_CANCELLED_REFUND', 5, u'zwrot po anulowaniu wydarzenia'),
        ('EVENT_CANCELLED_DEBIT', 6,
         u'obciążenie konta po anulowaniu wydarzenia'),
        ('EVENT_WON_PRIZE', 7, u'wygrana po rozstrzygnięciu wydarzenia'),
        ('TOPPED_UP_BY_APP', 8, u'doładowanie konta przez aplikację'),
    )

    # Transactions changing event price: BUY_YES, SELL_YES, BUY_NO, SELL_NO
    BUY_SELL_TYPES = (
        TRANSACTION_TYPE_CHOICES.BUY_YES,
        TRANSACTION_TYPE_CHOICES.SELL_YES,
        TRANSACTION_TYPE_CHOICES.BUY_NO,
        TRANSACTION_TYPE_CHOICES.SELL_NO,
    )

    objects = TransactionManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False,
                             related_name='transactions',
                             related_query_name='transaction')
    event = models.ForeignKey(Event, null=True, related_name='transactions',
                              related_query_name='transaction')
    type = models.PositiveIntegerField("rodzaj transakcji",
                                       choices=TRANSACTION_TYPE_CHOICES,
                                       default=1)
    date = models.DateTimeField('data', auto_now_add=True)
    quantity = models.PositiveIntegerField(u'ilość', default=1)
    price = models.IntegerField(u'cena jednostkowa', default=0, null=False)

    def __unicode__(self):
        return u'%s przez %s' % (self.TRANSACTION_TYPE_CHOICES[self.type].
                                 label, self.user)

    @property
    def total(self):
        """
        Get total price for all quantity in transaction: total won, total bought, total sold
        :return: total amount
        :rtype: int
        """
        return self.quantity * self.price

    class Meta:
        ordering = ['-date']
