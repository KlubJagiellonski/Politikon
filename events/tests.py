# -*- coding: utf-8 -*-
"""
Test events module
"""
from datetime import timedelta
import pytz

from django.test import TestCase
from django.utils.timezone import datetime

from .factories import EventFactory, ShortEventFactory, RefugeesEventFactory, \
    CruzEventFactory, BetFactory, TransactionFactory
from .models import Event
from .templatetags.format import formatted


class EventsModelTestCase(TestCase):
    """
    Test method for event
    """
    def test_event_creation(self):
        """
        Create event with minimal attributes
        """
        ShortEventFactory()
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
        self.assertTrue(event.is_in_progress)
        self.assertEqual({
            'event_id': 1,
            'buy_for_price': 50,
            'buy_against_price': 50,
            'sell_for_price': 50,
            'sell_against_price': 50
        }, event.event_dict)


class EventsManagerTestCase(TestCase):
    """
    events/managers EventManager
    """
    def test_get_events(self):
        """
        Get events
        """
        event1 = EventFactory\
            (turnover=1,
             absolute_price_change=1000,
             estimated_end_date=datetime.now(tz=pytz.UTC) + timedelta(days=2))
        event2 = RefugeesEventFactory\
            (outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS,
             turnover=3,
             absolute_price_change=3000,
             estimated_end_date=datetime.now(tz=pytz.UTC) + timedelta(days=1))
        event3 = CruzEventFactory\
            (turnover=2,
             absolute_price_change=2000,
             estimated_end_date=datetime.now(tz=pytz.UTC) + timedelta(days=4))
        event4 = EventFactory\
            (outcome=Event.EVENT_OUTCOME_CHOICES.FINISHED_YES,
             absolute_price_change=5000,
             estimated_end_date=datetime.now(tz=pytz.UTC) + timedelta(days=2))
        event5 = CruzEventFactory\
            (outcome=Event.EVENT_OUTCOME_CHOICES.FINISHED_NO)

        ongoing_events = Event.objects.ongoing_only_queryset()
        self.assertIsInstance(ongoing_events[0], Event)
        self.assertEqual(3, len(ongoing_events))
        self.assertEqual([event1, event2, event3], list(ongoing_events))

        popular_events = Event.objects.get_events('popular')
        self.assertIsInstance(popular_events[0], Event)
        self.assertEqual(3, len(popular_events))
        self.assertEqual([event2, event3, event1], list(popular_events))

        latest_events = Event.objects.get_events('latest')
        self.assertIsInstance(latest_events[0], Event)
        self.assertEqual(3, len(latest_events))
        self.assertEqual([event3, event2, event1], list(latest_events))

        changed_events = Event.objects.get_events('changed')
        self.assertIsInstance(changed_events[0], Event)
        self.assertEqual(3, len(changed_events))
        self.assertEqual([event2, event3, event1], list(changed_events))

        finished_events = Event.objects.get_events('finished')
        self.assertIsInstance(finished_events[0], Event)
        self.assertEqual(2, len(finished_events))
        self.assertEqual([event4, event5], list(finished_events))

    def test_get_front_event(self):
        """
        Get front event
        """
        front_event = Event.objects.get_front_event()
        self.assertIsNone(front_event)

        event1 = EventFactory()
        event2 = EventFactory()
        event3 = EventFactory(outcome=Event.EVENT_OUTCOME_CHOICES.CANCELLED)

        front_event = Event.objects.get_front_event()
        self.assertIsInstance(front_event, Event)
        self.assertEqual(event2, front_event)

    def test_get_featured_events(self):
        """
        Get featured events
        """
        event1 = EventFactory()
        event2 = EventFactory()
        event3 = EventFactory(outcome=Event.EVENT_OUTCOME_CHOICES.CANCELLED)

        featured_events = Event.objects.get_featured_events()
        self.assertIsInstance(featured_events[0], Event)
        self.assertEqual(2, len(featured_events))
        self.assertEqual([event1, event2], list(featured_events))


class EventsTemplatetagsTestCase(TestCase):
    """
    events/templatetags
    """
    def test_formatted(self):
        """
        Formatted templatetag
        """
        value = formatted(1000, True)
        self.assertEqual("+1 000", value)

        value = formatted(1000)
        self.assertEqual("1 000", value)

        value = formatted(-1000)
        self.assertEqual("-1 000", value)

        value = formatted(-100)
        self.assertEqual("-100", value)

        value = formatted(" ")
        self.assertEqual(" ", value)
