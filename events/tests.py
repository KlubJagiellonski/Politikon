# -*- coding: utf-8 -*-
"""
Test events module
"""
from datetime import timedelta
from freezegun import freeze_time
import json

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.translation import ugettext as _

from .exceptions import NonexistantEvent, PriceMismatch, EventNotInProgress, UnknownOutcome, \
    InsufficientCash, InsufficientBets, EventAlreadyFinished
from .factories import EventFactory, ShortEventFactory, BetFactory, TransactionFactory
from .models import Bet, Event, Transaction
from .tasks import create_open_events_snapshot, calculate_price_change
from .templatetags.display import render_bet, render_event, render_events, render_featured_event, \
    render_featured_events, render_bet_status, userstats, outcome, render_finish_date, og_title
from .views import transactions as bet_transactions

from accounts.factories import UserFactory
from politikon.templatetags.path import startswith


class EventsModelTestCase(TestCase):
    """
    Test methods for event
    """
    def test_event_creation(self):
        """
        Create event with minimal attributes
        """
        event = ShortEventFactory()
        self.assertIsInstance(event, Event)

    def test_event_with_attributes(self):
        """
        Create event with all attributes
        """
        event = EventFactory()
        self.assertIsInstance(event, Event)
        self.assertEqual(u'Długi tytuł testowego wydarzenia', event.title)
        self.assertEqual(u'Długi tytuł testowego wydarzenia',
                         event.__unicode__())
        self.assertEqual('/event/1-dlugi-tytul-testowego-wydarzenia',
                         event.get_relative_url())
        # TODO rename to politikon.org.pl
        self.assertEqual('http://example.com/event/1-a', event.get_absolute_url())
        self.assertTrue(event.is_in_progress)
        self.assertEqual('event_1', event.publish_channel)
        self.assertEqual({
            'event_id': 1,
            'buy_for_price': 50,
            'buy_against_price': 50,
            'sell_for_price': 50,
            'sell_against_price': 50
        }, event.event_dict)

        outcome1 = event.price_for_outcome('YES', 'BUY')
        self.assertEqual(event.current_buy_for_price, outcome1)
        outcome2 = event.price_for_outcome('YES', 'SELL')
        self.assertEqual(event.current_sell_for_price, outcome2)
        outcome3 = event.price_for_outcome('NO')
        self.assertEqual(event.current_buy_against_price, outcome3)
        outcome4 = event.price_for_outcome('NO', 'SELL')
        self.assertEqual(event.current_sell_against_price, outcome4)
        with self.assertRaises(UnknownOutcome):
            event.price_for_outcome('OOOPS', 'MY MISTAKE')

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_get_chart_points(self):
        """
        Get chart points
        """
        # time of get_chart_points
        initial_time = timezone.now().\
            replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=15)
        with freeze_time(initial_time) as frozen_time:
            event1 = EventFactory()
            event1.current_buy_for_price = 90
            event1.save()

            create_open_events_snapshot.delay()
            frozen_time.tick(delta=timedelta(days=3))

            event1.current_buy_for_price = 30
            event1.save()
            event2 = EventFactory()
            event2.current_buy_for_price = 30
            event2.save()

            create_open_events_snapshot.delay()
            frozen_time.tick(delta=timedelta(days=5))

            event1.current_buy_for_price = 60
            event1.save()
            event2.current_buy_for_price = 60
            event2.save()
            event3 = EventFactory()

            create_open_events_snapshot.delay()
            frozen_time.tick(delta=timedelta(days=2))

            event1.current_buy_for_price = 55
            event1.save()
            event2.current_buy_for_price = 55
            event2.save()
            event3.current_buy_for_price = 55
            event3.save()

            create_open_events_snapshot.delay()
            frozen_time.tick(delta=timedelta(days=2))

            event1.current_buy_for_price = 82
            event1.save()
            event2.current_buy_for_price = 82
            event2.save()
            event3.current_buy_for_price = 82
            event3.save()

            create_open_events_snapshot.delay()
            frozen_time.tick(delta=timedelta(days=2))
            event3.finish_yes()
            event3.save()

            # no snapshot now
            frozen_time.tick(delta=timedelta(days=1))
            event1.current_buy_for_price = 0
            event1.save()
            event2.current_buy_for_price = 0
            event2.save()

            create_open_events_snapshot.delay()

        # time of caculate_price_change task
        final_time = timezone.now().replace(hour=0, minute=1, second=0, microsecond=0)
        with freeze_time(final_time) as frozen_time:
            # TODO: do this better
            short_range = Event.EVENT_SMALL_CHART_DAYS
            first_date = timezone.now() - timedelta(days=short_range-1)
            days = [first_date + timedelta(n) for n in range(short_range)]
            labels = [
                u'{0} {1}'.format(step_date.day, _(step_date.strftime('%B'))) for step_date in days
            ]

            long_range = Event.EVENT_BIG_CHART_DAYS
            first_date2 = timezone.now() - timedelta(days=long_range-1)
            days2 = [first_date2 + timedelta(n) for n in range(long_range)]
            labels2 = [
                u'{0} {1}'.format(step_date.day, _(step_date.strftime('%B'))) for step_date in days2
            ]

            margin = [Event.BEGIN_PRICE] * Event.CHART_MARGIN
            mlen = len(margin)
            points1 = [90, 90, 90, 30, 30, 30, 30, 30, 60, 60, 55, 55, 82, 82, 82, 0]
            points2 = [30, 30, 30, 30, 30, 60, 60, 55, 55, 82, 82, 82, 0]
            points3 = [Event.BEGIN_PRICE, Event.BEGIN_PRICE, 55, 55, 82, 82, 82]
            self.assertEqual({
                'id': 1,
                'labels': labels,
                'points': points1[2:]
            }, event1.get_event_small_chart())
            self.assertEqual({
                'id': 1,
                # labels 3 ends one day earlier
                'labels': labels2[long_range-mlen-len(points1):],
                'points': margin + points1
            }, event1.get_event_big_chart())
            self.assertEqual({
                'id': 2,
                'labels': labels,
                'points': [Event.BEGIN_PRICE] + points2
            }, event2.get_event_small_chart())
            self.assertEqual({
                'id': 2,
                'labels': labels2[long_range-mlen-len(points2):],
                'points': margin + points2
            }, event2.get_event_big_chart())
            self.assertEqual({
                'id': 3,
                # labels 3 ends one day earlier
                'labels': labels[short_range-1-mlen-len(points3):short_range-1],
                'points': margin + points3
            }, event3.get_event_small_chart())
            self.assertEqual({
                'id': 3,
                # labels 3 ends one day earlier
                'labels': labels2[long_range-1-mlen-len(points3):long_range-1],
                'points': margin + points3
            }, event3.get_event_big_chart())

    def test_get_bet_social(self):
        """
        Get bet social
        """
        event = EventFactory()
        users_yes = UserFactory.create_batch(10)
        users_no = UserFactory.create_batch(10)
        bets_yes = [BetFactory(user=u, event=event) for u in users_yes]
        bets_no = [BetFactory(user=u, event=event, outcome=Bet.BET_OUTCOME_CHOICES.NO) \
                   for u in users_no]
        self.maxDiff = None
        social = event.get_bet_social()
        self.assertEqual(10, social['yes_count'])
        self.assertEqual(bets_yes[:6], list(social['yes_bets']))
        self.assertEqual(10, social['no_count'])
        self.assertEqual(bets_no[:6], list(social['no_bets']))

    def test_increment_quantity(self):
        """
        Increment quantity
        """
        amount = 2
        event = EventFactory(B=amount)
        start_event_dict = event.event_dict
        self.assertEqual(0, event.Q_for)
        self.assertEqual(0, event.Q_against)

        outcome_yes = 'YES'
        outcome_no = 'NO'

        # TODO check this on paper
        event.increment_quantity(outcome_yes, amount)
        self.assertEqual(amount, event.Q_for)
        self.assertEqual(0, event.Q_against)
        self.assertNotEqual(start_event_dict, event.event_dict)
        self.assertNotEqual(start_event_dict['buy_against_price'], event.event_dict['buy_against_price'])
        self.assertNotEqual(start_event_dict['buy_for_price'], event.event_dict['buy_for_price'])
        self.assertNotEqual(start_event_dict['buy_against_price'], event.event_dict['buy_against_price'])
        self.assertEqual(start_event_dict['sell_for_price'], event.event_dict['sell_for_price'])

        event.increment_quantity(outcome_no, amount)
        self.assertEqual(amount, event.Q_for)
        self.assertEqual(amount, event.Q_against)
        self.assertNotEqual(start_event_dict, event.event_dict)
        self.assertEqual(start_event_dict['buy_against_price'], event.event_dict['buy_against_price'])
        self.assertEqual(start_event_dict['buy_for_price'], event.event_dict['buy_for_price'])
        self.assertNotEqual(start_event_dict['sell_against_price'], event.event_dict['sell_against_price'])
        self.assertNotEqual(start_event_dict['sell_for_price'], event.event_dict['sell_for_price'])

        bad_outcome = 'OOOPS'
        with self.assertRaises(UnknownOutcome):
            event.increment_quantity(bad_outcome, amount)

    def test_increment_by_turnover(self):
        """
        Increment by turnover
        """
        event = EventFactory()
        self.assertEqual(0, event.turnover)

        event.increment_turnover(10)
        self.assertEqual(10, event.turnover)

        event.increment_turnover(-5)
        self.assertEqual(5, event.turnover)

    def test_finish_yes(self):
        """
        Finish event with outcome yes
        """
        users = UserFactory.create_batch(3)
        for u in users:
            u.portfolio_value = 1000
            u.total_cash = 2000
        event = EventFactory()
        bets = [BetFactory(event=event, user=user, has=3) for user in users[:2]]
        bets[1].outcome = Bet.BET_OUTCOME_CHOICES.NO
        bets[1].save()
        event.finish_yes()

        self.assertIsNotNone(event.end_date)
        self.assertEqual(Event.EVENT_OUTCOME_CHOICES.FINISHED_YES, event.outcome)

        event2 = EventFactory(outcome=Event.EVENT_OUTCOME_CHOICES.FINISHED_NO)
        with self.assertRaises(EventAlreadyFinished):
            event2.finish_yes()

    def test_finish_no(self):
        """
        Finish event with outcome no
        """
        event = EventFactory()
        event.finish_no()
        self.assertIsNotNone(event.end_date)
        self.assertEqual(Event.EVENT_OUTCOME_CHOICES.FINISHED_NO, event.outcome)

    def test_cancel(self):
        """
        Cancel event
        """
        # TODO:


class EventsManagerTestCase(TestCase):
    """
    events/managers EventManager
    """
    def test_ongoing_only_queryset(self):
        """
        Ongoing only queryset
        """
        events = EventFactory.create_batch(5)
        events[1].finish_yes()
        events[2].finish_no()
        events[3].cancel()
        self.assertEqual([events[0], events[4]], list(Event.objects.ongoing_only_queryset()))

    def test_get_events(self):
        """
        Get events
        """
        event1 = EventFactory(
            turnover=1,
            absolute_price_change=1000,
            estimated_end_date=timezone.now() + timedelta(days=2)
        )
        event2 = EventFactory(
            outcome=Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS,
            turnover=3,
            absolute_price_change=3000,
            estimated_end_date=timezone.now() + timedelta(days=1)
        )
        event3 = EventFactory(
            turnover=2,
            absolute_price_change=2000,
            estimated_end_date=timezone.now() + timedelta(days=4)
        )
        event4 = EventFactory(
            outcome=Event.EVENT_OUTCOME_CHOICES.FINISHED_YES,
            absolute_price_change=5000,
            estimated_end_date=timezone.now() + timedelta(days=2)
        )
        event5 = EventFactory(outcome=Event.EVENT_OUTCOME_CHOICES.FINISHED_NO)

        ongoing_events = Event.objects.ongoing_only_queryset()
        self.assertIsInstance(ongoing_events[0], Event)
        self.assertEqual(3, len(ongoing_events))
        self.assertEqual([event1, event2, event3], list(ongoing_events))

        popular_events = Event.objects.get_events('popular')
        self.assertIsInstance(popular_events[0], Event)
        self.assertEqual(3, len(popular_events))
        self.assertEqual([event2, event3, event1], list(popular_events))

        last_minute_events = Event.objects.get_events('last-minute')
        self.assertIsInstance(popular_events[0], Event)
        self.assertEqual(3, len(popular_events))
        self.assertEqual([event2, event1, event3], list(last_minute_events))

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

    def test_get_featured_events(self):
        """
        Get featured events
        """
        events = EventFactory.create_batch(7)
        events[2].outcome = Event.EVENT_OUTCOME_CHOICES.CANCELLED
        events[2].save()

        featured_events = Event.objects.get_featured_events()
        self.assertIsInstance(featured_events[0], Event)
        self.assertEqual(3, len(featured_events))
        self.assertEqual([events[4], events[5], events[6]], list(featured_events))

    def test_get_front_event(self):
        """
        Get front event
        """
        front_event = Event.objects.get_front_event()
        self.assertIsNone(front_event)

        events = EventFactory.create_batch(2)
        EventFactory(outcome=Event.EVENT_OUTCOME_CHOICES.CANCELLED)

        front_event = Event.objects.get_front_event()
        self.assertIsInstance(front_event, Event)

        events[1].outcome = Event.EVENT_OUTCOME_CHOICES.CANCELLED
        events[1].save()
        front_event = Event.objects.get_front_event()
        self.assertIsNone(front_event)


class EventsTasksTestCase(TestCase):
    """
    events/tasks
    """
    @staticmethod
    def _refresh_objects(objects):
        for obj in objects:
            obj.refresh_from_db()

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_create_open_events_snapshot(self):
        """
        Create open events snapshot
        """
        #  events = EventFactory.create_batch(5)
        EventFactory.create_batch(5)
        create_open_events_snapshot.delay()

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_calculate_price_change(self):
        """
        Calculate price change
        """
        initial_time = timezone.now().\
            replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=2)
        with freeze_time(initial_time) as frozen_time:
            events = EventFactory.create_batch(3)
            events[0].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_YES
            events[0].save()

            frozen_time.tick(delta=timedelta(days=1))
            events[1].current_buy_for_price = 60.0
            events[1].save()
            events[2].current_buy_for_price = 40.0
            events[2].save()
            calculate_price_change()
            self._refresh_objects(events)
            self.assertEqual(0, events[0].price_change)
            self.assertEqual(10, events[1].price_change)
            self.assertEqual(-10, events[2].price_change)

            create_open_events_snapshot()
            frozen_time.tick(delta=timedelta(days=1))
            events[1].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_NO
            events[1].save()
            events[2].current_buy_for_price = 100
            events[2].save()
            calculate_price_change()
            self._refresh_objects(events)
            self.assertEqual(0, events[0].price_change)
            self.assertEqual(10, events[1].price_change)
            self.assertEqual(60, events[2].price_change)


class EventsTemplatetagsTestCase(TestCase):
    """
    events/templatetags
    """
    def test_render_bet(self):
        """
        Render bet
        """
        event = EventFactory()
        user = UserFactory()
        bet = BetFactory(event=event, user=user)
        self.assertEqual({
            'event': event,
            'bet': bet,
            'render_current': True,
        }, render_bet(event, bet, True))

    def test_render_event(self):
        """
        Render event
        """
        event = EventFactory()
        user = UserFactory()
        bet = BetFactory(event=event, user=user)
        self.assertEqual({
            'event': event,
            'bet': bet,
        }, render_event(event, bet))

    def test_render_events(self):
        """
        Render events
        """
        events = EventFactory.create_batch(10)
        self.assertEqual({
            'events': events
        }, render_events(events))

    def test_render_featured_event(self):
        """
        Render events
        """
        event = EventFactory()
        self.assertEqual({
            'event': event
        }, render_featured_event(event))

    def test_render_featured_events(self):
        """
        Render events
        """
        events = EventFactory.create_batch(10)
        self.assertEqual({
            'events': events
        }, render_featured_events(events))

    def test_render_bet_status(self):
        """
        Render event
        """
        event = EventFactory()
        user = UserFactory()
        bet = BetFactory(event=event, user=user)
        self.assertEqual({
            'bet': bet,
        }, render_bet_status(bet))

    def test_userstats(self):
        """
        Userstats
        """
        user = UserFactory()
        overall_rank = 1
        month_rank = 1
        week_rank = 1
        self.assertEqual({
            'user': user,
            'overall_rank': overall_rank,
            'month_rank': month_rank,
            'week_rank': week_rank
        }, userstats(user, overall_rank, month_rank, week_rank))
        
    def test_outcome(self):
        """
        Outcome
        """
        events = EventFactory.create_batch(4)
        events[0].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_YES
        events[1].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_NO
        events[2].outcome = Event.EVENT_OUTCOME_CHOICES.CANCELLED
        self.assertEqual(" finished finished-yes", outcome(events[0]))
        self.assertEqual(" finished finished-no", outcome(events[1]))
        self.assertEqual(" finished finished-cancelled", outcome(events[2]))
        self.assertEqual("", outcome(events[3]))

    def test_render_finish_date(self):
        """
        Render finish date
        """
        events = EventFactory.create_batch(2)
        events[0].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_YES
        finish_time = timezone.now()
        events[0].end_date = finish_time
        future_time = timezone.now() + timedelta(days=8)
        events[1].estimated_end_date = future_time
        self.assertEqual({
            'date': finish_time,
            'is_in_progress': False
        }, render_finish_date(events[0]))
        self.assertEqual({
            'date': future_time,
            'is_in_progress': True
        }, render_finish_date(events[1]))

    def test_og_title(self):
        """
        OG title
        """
        user = UserFactory(name="Bromando")
        events = EventFactory.create_batch(3)
        events[0].title_fb_yes = u"będzie TAK"
        events[0].title_fb_no = u"nie będzie TAK"
        events[1].title_fb_yes = u"będzie TAK"
        events[1].title_fb_no = u"nie będzie TAK"
        events[2].title = u"Czy będzie TAK?"
        BetFactory(user=user, event=events[0])
        BetFactory(user=user, event=events[1], outcome=Bet.BET_OUTCOME_CHOICES.NO)
        self.assertEqual({
            'title': u'Bromando uważa że będzie TAK'
        }, og_title(events[0], user=user))
        self.assertEqual({
            'title': u'Bromando uważa że nie będzie TAK'
        }, og_title(events[1], user=user))
        self.assertEqual({
            'title': u'Moim zdaniem będzie TAK'
        }, og_title(events[0], vote=Bet.BET_OUTCOME_CHOICES.YES))
        self.assertEqual({
            'title': u'Moim zdaniem nie będzie TAK'
        }, og_title(events[1], vote=Bet.BET_OUTCOME_CHOICES.NO))
        self.assertEqual({
            'title': u'Czy będzie TAK?'
        }, og_title(events[2]))
        self.assertEqual({
            'title': u'Czy będzie TAK?'
        }, og_title(events[2], user=user))

        events[0].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_YES
        self.assertEqual({
            'title': u'Bromando ma rację że będzie TAK'
        }, og_title(events[0], user=user))
        self.assertEqual({
            'title': u'Mam rację że będzie TAK'
        }, og_title(events[0], vote=Bet.BET_OUTCOME_CHOICES.YES))

        events[1].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_NO
        self.assertEqual({
            'title': u'Bromando ma rację że nie będzie TAK'
        }, og_title(events[1], user=user))
        self.assertEqual({
            'title': u'Mam rację że nie będzie TAK'
        }, og_title(events[1], vote=Bet.BET_OUTCOME_CHOICES.NO))

        events[1].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_YES
        self.assertEqual({
            'title': u'Bromando nie ma racji że nie będzie TAK'
        }, og_title(events[1], user=user))
        self.assertEqual({
            'title': u'Nie mam racji że nie będzie TAK'
        }, og_title(events[1], vote=Bet.BET_OUTCOME_CHOICES.NO))


class BetsModelTestCase(TestCase):
    """
    Test methods for bet
    """
    def test_bet_creation(self):
        """
        Create a bet
        """
        event = EventFactory(title='wydarzenie')
        user = UserFactory(username='brode')
        bet = Bet(event=event, user=user, outcome=Bet.BET_OUTCOME_CHOICES.YES)
        bet.save()

        self.assertEqual({
            'bet_id': 1,
            'event_id': 1,
            'user_id': 1,
            'outcome': Bet.BET_OUTCOME_CHOICES.YES,
            'has': 0,
            'bought': 0,
            'sold': 0,
            'bought_avg_price': 0,
            'sold_avg_price': 0,
            'rewarded_total': 0
        }, bet.bet_dict)
        self.assertEqual(u'zakłady brode na wydarzenie', bet.__unicode__())

    def test_current_event_price(self):
        """
        Current event price
        """
        event = EventFactory()
        users = UserFactory.create_batch(2)
        bet1 = BetFactory(event=event, user=users[0], outcome=Bet.BET_OUTCOME_CHOICES.YES)
        bet2 = BetFactory(event=event, user=users[1], outcome=Bet.BET_OUTCOME_CHOICES.NO)
        event.current_buy_for_price = 55
        event.current_buy_against_price = 45
        self.assertEqual(55, bet1.current_event_price())
        self.assertEqual(45, bet2.current_event_price())

    def test_is_won(self):
        """
        Is won
        """
        events = EventFactory.create_batch(3)
        user = UserFactory()
        bet1 = BetFactory(event=events[0], user=user, outcome=Bet.BET_OUTCOME_CHOICES.YES)
        bet2 = BetFactory(event=events[1], user=user, outcome=Bet.BET_OUTCOME_CHOICES.YES)
        bet3 = BetFactory(event=events[2], user=user, outcome=Bet.BET_OUTCOME_CHOICES.YES)
        bet4 = BetFactory(event=events[2], user=user, outcome=Bet.BET_OUTCOME_CHOICES.NO)
        events[0].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_YES
        events[1].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_NO
        events[2].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_NO
        self.assertTrue(bet1.is_won())
        self.assertFalse(bet2.is_won())
        self.assertFalse(bet3.is_won())
        self.assertTrue(bet4.is_won())

    def test_get_wallet_change(self):
        """
        Get wallet change
        """
        # TODO this method is suspicious

    def test_get_invested(self):
        """
        Get invested
        """
        # TODO this method is suspicious

    def test_get_won(self):
        """
        Get won
        """
        events = EventFactory.create_batch(2)
        user = UserFactory()
        bet1 = BetFactory(event=events[0], user=user, outcome=Bet.BET_OUTCOME_CHOICES.YES, has=5)
        bet2 = BetFactory(event=events[1], user=user, outcome=Bet.BET_OUTCOME_CHOICES.YES, has=5)
        events[0].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_YES
        events[1].outcome = Event.EVENT_OUTCOME_CHOICES.FINISHED_NO
        self.assertEqual(500, bet1.get_won())
        self.assertEqual(0, bet2.get_won())

    def test_event_outcomes(self):
        """
        Is finished yes / no / cancelled
        """
        events = EventFactory.create_batch(4)
        user = UserFactory()
        bets = [BetFactory(user=user, event=e) for e in events]

        events[1].finish_yes()
        events[2].finish_no()
        events[3].cancel()
        self.assertFalse(bets[0].is_finished_yes())
        self.assertFalse(bets[0].is_finished_no())
        self.assertFalse(bets[0].is_cancelled())
        self.assertTrue(bets[1].is_finished_yes())
        self.assertTrue(bets[2].is_finished_no())
        self.assertTrue(bets[3].is_cancelled())


class BetsManagerTestCase(TestCase):
    """
    events/managers BetManager
    """
    def test_get_user_bets_for_events(self):
        """
        Get users bets for events
        """
        user = UserFactory()
        events = EventFactory.create_batch(3)
        bets = [BetFactory(user=user, event=e) for e in events]
        events[1].finish_yes()
        result = [bets[1], bets[2]]
        in_events = [events[1], events[2]]
        self.assertEqual(result, list(Bet.objects.get_user_bets_for_events(user, in_events)))

    def test_get_user_event_and_bet_for_update(self):
        """
        Get users event and bet for update
        """
        users = UserFactory.create_batch(2)
        events = EventFactory.create_batch(3)
        with self.assertRaises(NonexistantEvent):
            Bet.objects.get_user_event_and_bet_for_update(users[0], -1, 'YES')
        events[1].finish_yes()
        with self.assertRaises(EventNotInProgress):
            Bet.objects.get_user_event_and_bet_for_update(users[0], 2, 'YES')
        with self.assertRaises(UnknownOutcome):
            Bet.objects.get_user_event_and_bet_for_update(users[0], 1, 'OOOPS')
        new_bet = Bet.objects.get_user_event_and_bet_for_update(users[0], 1, 'YES')
        self.assertEqual(users[0], new_bet[0])
        self.assertEqual(events[0], new_bet[1])

        bet = BetFactory(user=users[1], event=events[2])
        self.assertEqual(
            (users[1], events[2], bet),
            Bet.objects.get_user_event_and_bet_for_update(users[1], 3, 'YES')
        )

    def test_buy_a_bet(self):
        """
        Buy a bet
        """
        event = EventFactory()
        user = UserFactory(total_cash=event.current_buy_for_price)
        old_price = event.current_buy_for_price
        bet_user, bet_event, bet = Bet.objects.buy_a_bet(user, event.id, 'YES',
                                                         event.current_buy_for_price)
        self.assertEqual(user, bet_user)
        self.assertEqual(event, bet_event)
        self.assertEqual(event.current_buy_for_price, bet.bought_avg_price)
        self.assertEqual(1, bet.has)
        self.assertEqual(1, bet.bought)
        self.assertEqual(0, bet_user.total_cash)
        self.assertEqual(old_price, bet_user.portfolio_value)
        self.assertNotEqual(old_price, bet_event.current_buy_for_price)
        self.assertEqual(1, bet_event.turnover)

        with self.assertRaises(PriceMismatch):
            Bet.objects.buy_a_bet(user, event.id, 'YES', old_price)

        with self.assertRaises(InsufficientCash):
            Bet.objects.buy_a_bet(user, event.id, 'YES', bet_event.current_buy_for_price)

        user.total_cash = bet_event.current_buy_against_price
        user.save()
        # TODO should throw exception
        Bet.objects.buy_a_bet(user, event.id, 'NO', bet_event.current_buy_against_price)

    def test_sell_a_bet(self):
        """
        Sell a bet
        """
        event = EventFactory()
        user = UserFactory(total_cash=event.current_buy_for_price)
        old_price = event.current_sell_for_price
        bet_user, bet_event, bet = Bet.objects.buy_a_bet(user, event.id, 'YES',
                                                         event.current_buy_for_price)
        avg_price = bet_event.current_sell_for_price

        with self.assertRaises(PriceMismatch):
            Bet.objects.sell_a_bet(user, event.id, 'YES', bet_event.current_buy_for_price)

        bet_user, bet_event, bet = Bet.objects.sell_a_bet(user, event.id, 'YES',
                                                          bet_event.current_sell_for_price)
        self.assertEqual(user, bet_user)
        self.assertEqual(event, bet_event)
        self.assertEqual(avg_price, bet.sold_avg_price)
        self.assertEqual(0, bet.has)
        self.assertEqual(1, bet.sold)
        self.assertEqual(old_price, bet_user.total_cash)
        self.assertEqual(0, bet_user.portfolio_value)
        self.assertEqual(old_price, bet_event.current_buy_for_price)
        self.assertEqual(2, bet_event.turnover)

        with self.assertRaises(InsufficientBets):
            Bet.objects.sell_a_bet(user, event.id, 'YES', bet_event.current_sell_for_price)

        bet_user, bet_event, bet = Bet.objects.buy_a_bet(user, event.id, 'NO',
                                                         event.current_buy_for_price)
        bet_user, bet_event, bet = Bet.objects.sell_a_bet(user, event.id, 'NO',
                                                          bet_event.current_sell_against_price)


    def test_get_in_progress(self):
        """
        Get in progress
        """
        user = UserFactory()
        events = EventFactory.create_batch(4)
        bets = [BetFactory(user=user, event=e, has=1) for e in events]
        bets[0].has = 0
        bets[0].save()
        events[2].finish_yes()
        self.assertEqual([bets[1], bets[3]], list(Bet.objects.get_in_progress()))

    def test_get_finished(self):
        """
        Get finished
        """
        user = UserFactory()
        events = EventFactory.create_batch(4)
        bets = [BetFactory(user=user, event=e, has=1) for e in events]
        bets[0].has = 0
        bets[0].save()
        events[1].finish_no()
        events[2].finish_yes()
        events[3].cancel()
        for e in events:
            e.save()
        self.assertEqual([bets[3], bets[2], bets[1]], list(Bet.objects.get_finished(user)))


class TransactionsModelTestCase(TestCase):
    """
    Test methods for transaction
    """
    def test_transaction_creation(self):
        """
        Create a transaction
        """
        user = UserFactory(username='mcbrover')
        event = EventFactory()
        transaction = TransactionFactory(
            user=user,
            event=event,
            type=Transaction.TRANSACTION_TYPE_CHOICES.BUY_YES
        )
        self.assertEqual(u'zakup udziałów na TAK przez mcbrover', transaction.__unicode__())
        self.assertEqual(0, transaction.total)
        transaction.quantity = 10
        transaction.price = 5
        self.assertEqual(50, transaction.total)


class TransactionManagerTestCase(TestCase):
    """
    events/managers TransactionManager
    """
    def test_get_user_transactions(self):
        """
        Get user transactions
        """
        user = UserFactory()
        events = EventFactory.create_batch(4)
        transactions = [TransactionFactory(user=user, event=e) for e in events]
        transactions[3].type = Transaction.TRANSACTION_TYPE_CHOICES.TOPPED_UP_BY_APP
        transactions[3].save()
        result = list(reversed(transactions[:3]))
        self.assertEqual(result, list(Transaction.objects.get_user_transactions(user)))

    def test_get_weekly_user_transactions(self):
        """
        Get weekly user transactions
        """
        initial_time = timezone.now() - timedelta(days=8)
        with freeze_time(initial_time) as frozen_time:
            user = UserFactory()
            events = EventFactory.create_batch(3)
            TransactionFactory(user=user, event=events[0])

            frozen_time.tick(delta=timedelta(days=3))
            transaction2 = TransactionFactory(user=user, event=events[1])

            frozen_time.tick(delta=timedelta(days=3))
            transaction3 = TransactionFactory(user=user, event=events[2])

        self.assertEqual(
            [transaction3, transaction2],
            list(Transaction.objects.get_weekly_user_transactions(user))
        )

    def test_get_monthly_user_transactions(self):
        """
        Get monthly user transactions
        """
        initial_time = timezone.now() - timedelta(days=32)
        with freeze_time(initial_time) as frozen_time:
            user = UserFactory()
            events = EventFactory.create_batch(3)
            TransactionFactory(user=user, event=events[0])

            frozen_time.tick(delta=timedelta(days=3))
            transaction2 = TransactionFactory(user=user, event=events[1])

            frozen_time.tick(delta=timedelta(days=3))
            transaction3 = TransactionFactory(user=user, event=events[2])

        self.assertEqual(
            [transaction3, transaction2],
            list(Transaction.objects.get_monthly_user_transactions(user))
        )


class PolitikonEventTemplatetagsTestCase(TestCase):
    """
    politikon/templatetags
    """
    def test_startswith(self):
        """
        Startswith
        """
        start_path = reverse('events:events')
        path1 = reverse('events:events')
        self.assertTrue(startswith(path1, start_path))
        path2 = reverse('events:events', kwargs={'mode': 'popular'})
        self.assertTrue(startswith(path2, start_path))
        path3 = reverse('events:events', kwargs={'mode': 'latest'})
        self.assertTrue(startswith(path3, start_path))
        path4 = reverse('events:events', kwargs={'mode': 'changed'})
        self.assertTrue(startswith(path4, start_path))
        path5 = reverse('events:events', kwargs={'mode': 'last-minute'})
        self.assertTrue(startswith(path5, start_path))


class EventsViewTestCase(TestCase):
    """
    Tests views methods
    """
    def test_transaction_url(self):
        """
        Test transactions ajax url and view for pagination
        """
        user = UserFactory()
        event = EventFactory()
        TransactionFactory(user=user, event=event)
        TransactionFactory(user=user, event=event)
        TransactionFactory(user=user, event=event)
        path = reverse('events:transactions', kwargs={'user_id': user.id, 'nr_from': 0})
        self.assertEqual(u'/transactions/1/0/', path)

        # get 2 of 3 transactions
        response = bet_transactions(None, user.id, 1)
        ts = json.loads(response.content)
        self.assertEqual(2, len(ts))

        # one transaction must have these keys:
        expected_keys = ['date', 'title', 'total', 'type_display']
        self.assertEqual(expected_keys, sorted(ts[0].keys()))
        self.assertEqual(expected_keys, sorted(ts[1].keys()))

