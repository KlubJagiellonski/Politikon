# -*- coding: utf-8 -*-
import factory
import pytz

from django.utils.timezone import datetime

from .models import Event, RelatedEvent, Bet, Transaction


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    estimated_end_date = datetime.now(tz=pytz.UTC)
    title = u'Długi tytuł testowego wydarzenia'
    short_title = u'Tytuł wydarzenia'
    title_fb_yes = u'Tytuł na tak'
    title_fb_no = u'Tytuł na nie'
    description = u'Opis wydarzenia testowego.'
    is_front = True
    is_featured = True
    outcome = Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS


class ShortEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    estimated_end_date = datetime.now(tz=pytz.UTC)


class RelatedEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RelatedEvent


class BetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bet

    has = 1
    bought = 1
    outcome = Bet.BET_OUTCOME_CHOICES.YES


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
