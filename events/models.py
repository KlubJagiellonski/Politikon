# coding: utf-8

from django.conf import settings
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.db import transaction
from django.utils.translation import ugettext as _

from django.template.defaultfilters import slugify
from unidecode import unidecode

from collections import defaultdict
from math import exp

from bladepolska.snapshots import SnapshotAddon
from bladepolska.site import current_domain
from bladepolska.pubnub import PubNub
from .exceptions import *


class EventManager(models.Manager):
    def ongoing_only_queryset(self):
        allowed_outcome = EVENT_OUTCOMES_DICT['IN_PROGRESS']
        return self.filter(outcome=allowed_outcome)

    def get_events(self, mode):
        if mode == 'popular':
            return self.ongoing_only_queryset().order_by('turnover')
        elif mode == 'latest':
            return self.ongoing_only_queryset().order_by('-created_date')
        elif mode == 'changed':
            return self.ongoing_only_queryset().order_by('-absolute_price_change')
        elif mode == 'finished':
            excluded_outcome = EVENT_OUTCOMES_DICT['IN_PROGRESS']
            return self.exclude(outcome=excluded_outcome).order_by('-end_date')

    def get_featured_events(self):
        return self.ongoing_only_queryset().filter(is_featured=True).order_by('estimated_end_date')

    def get_front_event(self):
        front_events = self.ongoing_only_queryset().filter(is_front=True).order_by('estimated_end_date')
        if front_events.count()>0:
            return front_events[0]
        else:
            return None

    def associate_people_with_events(self, user, events_list):
        event_ids = set([e.id for e in events_list])
        # friends = user.friends.all()
        bets = Bet.objects.select_related('user__facebook_user__profile_photo').filter(user__in=user.friends_ids_set, event__in=event_ids, has__gt=0)

        result = {
                    event_id: defaultdict(list)
                        # { outcome: defaultdict(list) for outcome in BET_OUTCOMES_DICT.keys() }
                            for event_id in event_ids
                 }

        for bet in bets:
            outcome = BET_OUTCOMES_INV_DICT[bet.outcome]
            result[bet.event_id][outcome].append(bet.user)

        return result


class BetManager(models.Manager):
    def get_users_bets_for_events(self, user, events):
        bets = self.filter(user__id=user.id, event__in=events)

        return bets

    def get_user_event_and_bet_for_update(self, user, event_id, for_outcome):
        event = list(Event.objects.select_for_update().filter(id=event_id))
        try:
            event = event[0]
        except IndexError:
            raise NonexistantEvent(_("Requested event does not exist."))

        if not event.is_in_progress:
            raise EventNotInProgress(_("Event is no longer in progress."))

        if for_outcome not in BET_OUTCOMES_DICT:
            raise UnknownOutcome()

        bet_outcome = BET_OUTCOMES_DICT[for_outcome]
        bet, created = self.get_or_create(user_id=user.id, event_id=event.id, outcome=bet_outcome)
        bet = list(self.select_for_update().filter(id=bet.id))[0]

        user = list(auth.get_user_model().objects.select_for_update().filter(id=user.id))[0]

        return user, event, bet

    def buy_a_bet(self, user, event_id, for_outcome, price):
        """ Always remember about wrapping this in a transaction! """
        user, event, bet = self.get_user_event_and_bet_for_update(user, event_id, for_outcome)

        if for_outcome == 'YES':
            transaction_type = TRANSACTION_TYPES_DICT['BUY_YES']
        else:
            transaction_type = TRANSACTION_TYPES_DICT['BUY_NO']

        requested_price = price
        current_tx_price = event.price_for_outcome(for_outcome, direction='BUY')
        if requested_price != current_tx_price:
            raise PriceMismatch(_("Price has changed."), event)

        quantity = 1
        bought_for_total = current_tx_price * quantity

        if (user.total_cash < bought_for_total):
            raise InsufficientCash(_("You don't have enough cash."), user)

        transaction = Transaction.objects.create(
                        user_id=user.id, event_id=event.id, type=transaction_type,
                        quantity=quantity, price=current_tx_price)

        event_total_bought_price = (bet.bought_avg_price * bet.bought)
        after_bought_quantity = bet.bought + quantity

        bet.bought_avg_price = (event_total_bought_price + bought_for_total) / after_bought_quantity
        bet.has += quantity
        bet.bought += quantity
        bet.save(update_fields=['bought_avg_price', 'has', 'bought'])

        user.total_cash -= bought_for_total
        user.save(update_fields=['total_cash'])

        event.increment_quantity(for_outcome, by_amount=quantity)
        """ Increment turnover only for buying bets """
        event.increment_turnover(quantity)
        event.save(force_update=True)

        from canvas.models import ActivityLog
        ActivityLog.objects.register_transaction_activity(user, transaction)

        PubNub().publish({
            'channel': event.publish_channel,
            'message': {
                'updates': {
                    'events': [event.event_dict]
                }
            }
        })

        return user, event, bet

    def sell_a_bet(self, user, event_id, for_outcome, price):
        """ Always remember about wrapping this in a transaction! """
        user, event, bet = self.get_user_event_and_bet_for_update(user, event_id, for_outcome)

        requested_price = price
        current_tx_price = event.price_for_outcome(for_outcome, direction='SELL')
        if requested_price != current_tx_price:
            raise PriceMismatch(_("Price has changed."), event)

        quantity = 1
        sold_for_total = current_tx_price * quantity

        if (bet.has < quantity):
            raise InsufficientBets(_("You don't have enough shares."), bet)

        if for_outcome == 'YES':
            transaction_type = TRANSACTION_TYPES_DICT['SELL_YES']
        else:
            transaction_type = TRANSACTION_TYPES_DICT['SELL_NO']

        transaction = Transaction.objects.create(
                        user_id=user.id, event_id=event.id, type=transaction_type,
                        quantity=quantity, price=current_tx_price)

        event_total_sold_price = (bet.sold_avg_price * bet.sold)
        after_sold_quantity = bet.sold + quantity

        bet.sold_avg_price = (event_total_sold_price + sold_for_total) / after_sold_quantity
        bet.has -= quantity
        bet.sold += quantity
        bet.save(update_fields=['sold_avg_price', 'has', 'sold'])

        user.total_cash += sold_for_total
        user.save(update_fields=['total_cash'])

        event.increment_quantity(for_outcome, by_amount=-quantity)
        event.save(force_update=True)

        from canvas.models import ActivityLog
        ActivityLog.objects.register_transaction_activity(user, transaction)

        PubNub().publish({
            'channel': event.publish_channel,
            'message': {
                'updates': {
                    'events': [event.event_dict]
                }
            }
        })

        return user, event, bet


class TransactionManager(models.Manager):
    pass

EVENT_OUTCOMES_DICT = {
    'IN_PROGRESS': 1,
    'CANCELLED': 2,
    'FINISHED_YES': 3,
    'FINISHED_NO': 4,
}

EVENT_OUTCOMES = [
    (1, u'w trakcie'),
    (2, u'anulowane'),
    (3, u'rozstrzygnięte na TAK'),
    (4, u'rozstrzygnięte na NIE'),
]

class Event(models.Model):
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

    title = models.TextField(u"tytuł wydarzenia")
    short_title = models.TextField(u"tytuł promocyjny wydarzenia")

    title_fb_yes = models.TextField(u"tytuł na TAK obiektu FB")
    title_fb_no = models.TextField(u"tytuł na NIE obiektu FB")

    description = models.TextField(u"pełny opis wydarzenia", default='')

    small_image = models.ImageField(u"mały obrazek 340x250", upload_to="events_small", null=True)
    big_image = models.ImageField(u"duży obrazek 1250x510", upload_to="events_big", null=True)

    is_featured = models.BooleanField(u"featured", default=False)
    is_front = models.BooleanField(u"front", default=False)
    outcome = models.PositiveIntegerField(u"rozstrzygnięcie", choices=EVENT_OUTCOMES, default=1)

    created_date = models.DateTimeField(auto_now_add=True)
    estimated_end_date = models.DateTimeField(u"przewidywana data rozstrzygnięcia")
    end_date = models.DateTimeField(u"data rozstrzygnięcia", null=True)

    current_buy_for_price = models.IntegerField(u"cena nabycia akcji zdarzenia", default=50.0)
    current_buy_against_price = models.IntegerField(u"cena nabycia akcji zdarzenia przeciwnego", default=50.0)
    current_sell_for_price = models.IntegerField(u"cena sprzedaży akcji zdarzenia", default=50.0)
    current_sell_against_price = models.IntegerField(u"cena sprzedaży akcji zdarzenia przeciwnego", default=50.0)

    last_transaction_date = models.DateTimeField(u"data ostatniej transakcji", null=True)

    Q_for = models.IntegerField(u"zakładów na TAK", default=0)
    Q_against = models.IntegerField(u"zakładów na NIE", default=0)
    turnover = models.IntegerField(u"obrót", default=0, db_index=True)

    absolute_price_change = models.IntegerField(u"zmiana ceny (wartość absolutna)", db_index=True, default=0)
    price_change = models.IntegerField(u"zmiana ceny", default=0)

    B = models.FloatField(u"stała B", default=5)

    def get_relative_url(self):
        return "/event/%(id)d-%(title)s" % { 'id' : self.id, 'title': slugify(unidecode(self.title))}

    def get_absolute_url(self):
        return "http://%(domain)s%(url)s" % {
            'domain': current_domain(),
            'url': reverse("events:event_detail", kwargs={'event_id': self.id})
        }

    def get_absolute_facebook_object_url(self):
        return "http://%(domain)s%(url)s" % {
            'domain': current_domain(),
            'url': reverse("events:event_facebook_object_detail", kwargs={'event_id': self.id})
        }

    @property
    def is_in_progress(self):
        return self.outcome == EVENT_OUTCOMES_DICT['IN_PROGRESS']

    @property
    def publish_channel(self):
        return "event_%d" % self.id

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
        if (direction, outcome) not in BET_OUTCOMES_TO_PRICE_ATTR:
            raise UnknownOutcome()

        attr = BET_OUTCOMES_TO_PRICE_ATTR[(direction, outcome)]
        return getattr(self, attr)

    def increment_quantity(self, outcome, by_amount):
        if outcome not in BET_OUTCOMES_TO_QUANTITY_ATTR:
            raise UnknownOutcome()

        attr = BET_OUTCOMES_TO_QUANTITY_ATTR[outcome]
        setattr(self, attr, getattr(self, attr) + by_amount)

        self.recalculate_prices()

    def increment_turnover(self, by_amount):
        self.turnover += by_amount;

    def recalculate_prices(self):
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

        self.current_buy_for_price = round(factor * buy_for_price,0)
        self.current_buy_against_price = round(factor * buy_against_price,0)
        self.current_sell_for_price = round(factor * sell_for_price,0)
        self.current_sell_against_price = round(factor * sell_against_price,0)

    def save(self, **kwargs):
        if not self.id:
            self.recalculate_prices()

        super(Event, self).save(**kwargs)


BET_OUTCOMES_DICT = {
    'YES': True,
    'NO': False,
}

BET_OUTCOMES_INV_DICT = {
    True: 'YES',
    False: 'NO',
}

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

BET_OUTCOMES = [
    (True, 'udziały na TAK'),
    (False, 'udziały na NIE'),
]


class Bet(models.Model):
    objects = BetManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    event = models.ForeignKey(Event, null=False)
    outcome = models.BooleanField("zakład na TAK", choices=BET_OUTCOMES)
    has = models.PositiveIntegerField(u"posiadane zakłady", default=0, null=False)
    bought = models.PositiveIntegerField(u"kupione zakłady", default=0, null=False)
    sold = models.PositiveIntegerField(u"sprzedane zakłady", default=0, null=False)
    bought_avg_price = models.FloatField(u"kupione po średniej cenie", default=0, null=False)
    sold_avg_price = models.FloatField(u"sprzedane po średniej cenie", default=0, null=False)
    rewarded_total = models.IntegerField(u"nagroda za wynik", default=0, null=False)

    @property
    def bet_dict(self):
        return {
            'bet_id': self.id,
            'event_id': self.event.id,
            'user_id': self.user.id,
            'outcome': BET_OUTCOMES_INV_DICT[self.outcome],
            'has': self.has,
            'bought': self.bought,
            'sold': self.sold,
            'bought_avg_price': self.bought_avg_price,
            'sold_avg_price': self.sold_avg_price,
            'rewarded_total': self.rewarded_total,
        }


TRANSACTION_TYPES_DICT = {
    'BUY_YES': 1,
    'SELL_YES': 2,
    'BUY_NO': 3,
    'SELL_NO': 4,
    'EVENT_CANCELLED_REFUND': 5,
    'EVENT_WON_PRIZE': 6,
    'TOPPED_UP_BY_APP': 7,
}

TRANSACTION_TYPES = (
    (1, 'zakup udziałów na TAK'),
    (2, 'sprzedaż udziałów na TAK'),
    (3, 'zakup udziałów na NIE'),
    (4, 'sprzedaż udziałów na NIE'),
    (5, 'zwrot po anulowaniu wydarzenia'),
    (6, 'wygrana po rozstrzygnięciu wydarzenia'),
    (7, 'doładowanie konta przez aplikację'),
)

TRANSACTION_TYPES_INV_DICT = {v: k for k, v in TRANSACTION_TYPES_DICT.items()}


class Transaction(models.Model):
    objects = TransactionManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    event = models.ForeignKey(Event, null=True)
    type = models.PositiveIntegerField("rodzaj transakcji", choices=TRANSACTION_TYPES, default=1)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(u"ilość", default=1)
    price = models.IntegerField(u"cena jednostkowa", default=0, null=False)
