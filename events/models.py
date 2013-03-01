# coding: utf-8

from django.db import models
from django.utils.translation import ugettext as _

from math import exp

from fandjango.models import User
from .exceptions import *


def round_price(price):
    return round(price, 2)


class EventManager(models.Manager):
    def ongoing_only_queryset(self):
        allowed_outcome = EVENT_OUTCOMES_DICT['IN_PROGRESS']
        return self.filter(outcome=allowed_outcome)

    def get_latest_events(self):
        return self.ongoing_only_queryset().order_by('-created_date')

    def get_featured_events(self):
        return self.ongoing_only_queryset().filter(is_featured=True).order_by('-created_date')


class BetManager(models.Manager):
    def get_users_bets(self, user):
        bets = self.select_related('event_set').filter(user=user)

        return bets

    def get_event_and_bet_for_update(user, event_id, for_outcome):
        event = list(Event.objects.select_for_update().filter(id=event_id))
        try:
            event = event[0]
        except IndexError:
            raise NonexistantEvent(_("Requested event does not exist."))

        if not event.is_in_progress:
            raise EventNotInProgress(_("Event is no longer in progress."))

        bet = self.get_or_create(user=user, event_id=event, outcome=for_outcome)
        bet = self.select_for_update().filter(id=bet_id)[0]

        return event, bet

    def buy_a_bet(user, event_id, for_outcome, price):
        event, bet = self.get_event_and_bet_for_update(user, event_id, for_outcome)

        requested_price = round_price(price)
        current_true_price = event.price_for_outcome(for_outcome)
        if requested_price != current_true_price:
            raise PriceMismatch(_("Price has changed."))

        quantity = 1

        Transaction.objects.create_transaction(user, event_id, for_outcome, current_true_price, direction="BUY", quantity=quantity)

        event_total_bought_price = (bet.bought_avg_price * bet.bought)
        bought_for_total = current_true_price * quantity
        after_bought_quantity = bet.bought + quantity

        bet.bought_avg_price = (event_total_bought_price + bought_for_total) / after_bought_quantity
        bet.has += quantity
        bet.bought += quantity

        bet.save(force_update=True)

        event.increment_quantity(for_outcome, by_amount=quantity)
        event.save(force_update=True)

        # @TODO: PubNub, ActivityLog

    def sell_a_bet(user, event_id, for_outcome, price):
        event, bet = self.get_event_and_bet_for_update(user, event_id, for_outcome)

        requested_price = round_price(price)
        current_true_price = event.price_for_outcome(for_outcome)
        if requested_price != current_true_price:
            raise PriceMismatch(_("Price has changed."))

        quantity = 1

        Transaction.objects.create_transaction(user, event_id, for_outcome, current_true_price, direction="SELL", quantity=quantity)

        event_total_sold_price = (bet.sold_avg_price * bet.sold)
        sold_for_total = current_true_price * quantity
        after_sold_quantity = bet.sold + quantity

        bet.sold_avg_price = (event_total_sold_price + sold_for_total) / after_sold_quantity
        bet.has -= quantity
        bet.sold += quantity

        bet.save(force_update=True)

        event.increment_quantity(for_outcome, by_amount=quantity)
        event.save(force_update=True)

        # @TODO: PubNub, ActivityLog


class TransactionManager(models.Manager):
    pass


EVENT_OUTCOMES_DICT = {
    'IN_PROGRESS': 1,
    'CANCELLED': 2,
    'FINISHED_YES': 3,
    'FINISHED_NO': 4,
}

EVENT_OUTCOMES = [
    (1, 'w trakcie'),
    (2, 'anulowane'),
    (3, 'rozstrzygnięte na TAK'),
    (4, 'rozstrzygnięte na NIE'),
]


class Event(models.Model):
    objects = EventManager()

    title = models.TextField(u"tytuł wydarzenia")
    short_title = models.TextField(u"tytuł promocyjny wydarzenia")
    descrition = models.TextField(u"pełny opis wydarzenia")

    small_image = models.ImageField(u"mały obrazek", upload_to="events_small", null=True)
    big_image = models.ImageField(u"duży obrazek", upload_to="events_big", null=True)

    is_featured = models.BooleanField(u"featured", default=False)
    outcome = models.PositiveIntegerField(u"rozstrzygnięcie", choices=EVENT_OUTCOMES, default=1)

    created_date = models.DateTimeField(auto_now_add=True)
    estimated_end_date = models.DateTimeField(u"data rozstrzygnięcia")

    current_buy_for_price = models.FloatField(u"cena akcji zdarzenia", default=50.0)
    current_buy_against_price = models.FloatField(u"cena akcji zdarzenia przeciwnego", default=50.0)

    last_transaction_date = models.DateTimeField(u"data ostatniej transakcji", null=True)

    Q_for = models.IntegerField(u"zakładów na TAK", default=0)
    Q_against = models.IntegerField(u"zakładów na NIE", default=0)

    B = models.FloatField(u"stała B", default=5)

    @property
    def is_in_progress(self):
        return self.outcome == EVENT_OUTCOMES_DICT['IN_PROGRESS']

    def price_for_outcome(self, outcome):
        if outcome not in BET_OUTCOMES_TO_PRICE_ATTR:
            raise UnknownOutcome()

        attr = BET_OUTCOMES_TO_PRICE_ATTR[outcome]
        return getattr(self, attr)

    def increment_quantity(self, outcome, by_amount):
        if outcome not in BET_OUTCOMES_TO_QUANTITY_ATTR:
            raise UnknownOutcome()

        attr = BET_OUTCOMES_TO_QUANTITY_ATTR[outcome]
        setattr(self, attr, getattr(self, attr) + 1)

        self.recalculate_prices()

    def recalculate_prices(self):
        e_for = exp(self.Q_for / self.B)
        e_against = exp(self.Q_against / self.B)
        buy_for_price = e_for / (e_for + e_against)
        buy_against_price = e_against / (e_for + e_against)

        self.current_buy_for_price = round_price(buy_for_price)
        self.current_buy_against_price = round_price(buy_against_price)

    def save(self, **kwargs):
        if not self.id:
            self.recalculate_prices()

        super(Event, self).save()


BET_OUTCOMES_DICT = {
    'YES': True,
    'NO': False,
}

BET_OUTCOMES_TO_PRICE_ATTR = {
    'YES': 'current_buy_for_price',
    'NO': 'current_buy_against_price'
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

    user = models.ForeignKey(User, null=False)
    event = models.ForeignKey(Event, null=False)
    outcome = models.BooleanField("zakład na TAK", choices=BET_OUTCOMES)
    has = models.PositiveIntegerField(u"posiadane zakłady", default=0, null=False)
    bought = models.PositiveIntegerField(u"kupione zakłady", default=0, null=False)
    sold = models.PositiveIntegerField(u"sprzedane zakłady", default=0, null=False)
    bought_avg_price = models.FloatField(u"kupione po średniej cenie", default=0, null=False)
    sold_avg_price = models.FloatField(u"sprzedane po średniej cenie", default=0, null=False)
    rewarded_total = models.FloatField(u"nagroda za wynik", default=0, null=False)


TRANSACTION_TYPES_DICT = {
    'BUY_YES': 1,
    'SELL_YES': 2,
    'BUY_NO': 3,
    'SELL_NO': 4,
    'EVENT_CANCELLED_REFUND': 5,
    'EVENT_WON_PRIZE': 6,
}

TRANSACTION_TYPES = [
    (1, 'zakup udziałów na TAK'),
    (2, 'sprzedaż udziałów na TAK'),
    (3, 'zakup udziałów na NIE'),
    (4, 'sprzedaż udziałów na NIE'),
    (5, 'zwrot po anulowaniu wydarzenia'),
    (6, 'wygrana po rozstrzygnięciu wydarzenia'),
]


class Transaction(models.Model):
    objects = TransactionManager()

    user = models.ForeignKey(User, null=False)
    event = models.ForeignKey(Event, null=False)
    type = models.PositiveIntegerField("rodzaj transakcji", choices=TRANSACTION_TYPES, default=1)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(u"ilość", default=1)
    price = models.PositiveIntegerField(u"cena jednostkowa", default=0, null=False)
