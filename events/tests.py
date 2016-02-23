# -*- coding: utf-8 -*-
"""
Test events module
"""
import pytz
from datetime import timedelta
from django.utils.timezone import datetime

from django.test import TestCase

from .models import Event


class EventsModelTestCase(TestCase):
    """
    Test method for event
    """
    def test_event_creation(self):
        """
        Create event with minimal attributes
        """
        Event.objects.create(
            estimated_end_date=datetime.now(tz=pytz.UTC)
        )
        e1 = Event.objects.all()[0]
        self.assertIsInstance(e1, Event)

    def test_event_with_attributes(self):
        """
        Create event with all attributes
        """
        Event.objects.create(
            estimated_end_date=datetime.now(tz=pytz.UTC),
            title='Długi tytuł testowego wydarzenia',
            short_title='Tytuł wydarzenia',
            title_fb_yes='Tytuł na tak',
            title_fb_no='Tytuł na nie',
            description='Opis wydarzenia testowego.'
        )
        e1 = Event.objects.all()[0]
        self.assertIsInstance(e1, Event)
        self.assertEqual(u'Długi tytuł testowego wydarzenia', e1.title)


