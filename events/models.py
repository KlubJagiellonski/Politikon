# coding: utf-8

from django.db import models

from fandjango.models import User


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

    current_buy_price = models.FloatField(u"cena akcji zdarzenia", default=50.0)
    current_sell_price = models.FloatField(u"cena akcji zdarzenia przeciwnego", default=50.0)

    last_transaction_date = models.DateTimeField(u"data ostatniej transakcji", null=True)

    Q_for = models.IntegerField(u"zakładów na TAK", default=0)
    Q_against = models.IntegerField(u"zakładów na NIE", default=0)

    B = models.FloatField(u"stała B", default=5)


class Bet(models.Model):
    objects = BetManager()

    user = models.ForeignKey(User, null=False)
    event = models.ForeignKey(Event, null=False)
    outcome = models.BooleanField("zakład na TAK")
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
    user = models.ForeignKey(User, null=False)
    event = models.ForeignKey(Event, null=False)
    type = models.PositiveIntegerField("rodzaj transakcji", choices=TRANSACTION_TYPES, default=1)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(u"ilość", default=1)
    price = models.PositiveIntegerField(u"cena jednostkowa", default=0, null=False)
