# -*- coding: utf-8 -*-
"""
Test events module
"""
from datetime import timedelta
from django.utils.timezone import datetime

from django.test import TestCase

from .factories import EventFactory, BetFactory, TransactionFactory
from .models import Event


class EventsModelTestCase(TestCase):
    """
    Test method for event
    """
    def test_event_creation(self):
        """
        Create event with minimal attributes
        """
        EventFactory()
        event = Event.objects.all()[0]
        self.assertIsInstance(event, Event)

    def test_event_with_attributes(self):
        """
        Create event with all attributes
        """
        EventFactory()
        event = Event.objects.all()[0]
        self.assertIsInstance(event, Event)
        self.assertEqual(u'Długi tytuł testowego wydarzenia', event.title)
        self.assertEqual(u'Długi tytuł testowego wydarzenia',
                         event.__unicode__())
        self.assertEqual('/event/1-dlugi-tytul-testowego-wydarzenia',
                         event.get_relative_url())
        self.assertEqual('/event/1-a', event.get_absolute_url())
        self.assertEqual(True, event.is_in_progress)
        self.assertEqual({
            'event_id': 1,
            'buy_for_price': 50,
            'buy_against_price': 50,
            'sell_for_price': 50,
            'sell_against_price': 50
        }, event.event_dict)
