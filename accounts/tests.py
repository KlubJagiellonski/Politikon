# -*- coding: utf-8 -*-
"""
Test accounts module
"""
import os
from decimal import Decimal
from mock import patch

from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.test import TestCase

from .factories import UserFactory, UserWithAvatarFactory, AdminFactory
from .models import UserProfile, get_image_path
from .tasks import topup_accounts_task, update_portfolio_value, create_accounts_snapshot, \
    update_users_classification
from .templatetags.user import user_home, user_rank
from .utils import process_username

from constance import config

from events.factories import EventFactory, BetFactory
from events.models import Event, Bet
from politikon.templatetags.format import formatted
from politikon.templatetags.path import startswith


class UserProfileModelTestCase(TestCase):
    """
    Test methods for user object
    """
    def test_user_creation(self):
        """
        Create user and check his attributes
        """
        user = UserFactory(username='johnsmith', name='John Smith')

        self.assertEqual('johnsmith', user.__unicode__())
        self.assertEqual('John Smith', user.name)
        self.assertEqual('John Smith', user.get_short_name())
        self.assertEqual(False, user.is_vip)
        self.assertEqual('John Smith (johnsmith)', user.get_full_name())
        self.assertEqual('John Smith (johnsmith)', user.full_name)
        user.calculate_reputation()
        user.save()
        self.assertEqual(False, user.is_superuser)
        self.assertEqual({
            'user_id': 1,
            'total_cash': formatted(0),
            'portfolio_value': formatted(0),
            'reputation': '100%',
        }, user.statistics_dict)
        self.assertEqual(0, user.current_portfolio_value)

    def test_get_image_path(self):
        """
        Get image path
        """
        user = UserFactory(username='johnsmith')

        path = get_image_path(user, 'my-avatar.png')
        self.assertEqual('avatars/johnsmith.png', path)

    def test_user_urls(self):
        """
        Check is urls are valid
        """
        user = UserFactory(
            twitter_user='jsmith',
            facebook_user='facesmith'
        )

        # TODO: FIXME
        # url = user.get_absolute_url()
        # self.assertEqual('/accounts/1/', url)
        #
        # url = user.get_avatar_url()
        # self.assertEqual('/static/img/blank-avatar.jpg', url)
        #
        # url = user.get_twitter_url()
        # self.assertEqual('https://twitter.com/jsmith', url)
        #
        # url = user.get_facebook_url()
        # self.assertEqual('https://www.facebook.com/facesmith', url)

    def test_twitter_user(self):
        """
        Check method for account connected with twitter
        """
        user = UserFactory()

        url = user.get_facebook_url()
        self.assertIsNone(url)

        url = user.get_twitter_url()
        self.assertIsNone(url)

        user.twitter_user = 'jsmith'
        user.save()

        url = user.get_twitter_url()
        self.assertEqual('https://twitter.com/jsmith', url)

    def test_current_portfolio_value(self):
        """
        Current portfolio value
        """
        user = UserFactory()
        self.assertEqual(0, user.current_portfolio_value)
        event = EventFactory()
        bet = BetFactory(user=user, event=event)
        self.assertEqual(50, user.current_portfolio_value)
        bet.outcome = Bet.NO
        bet.has = 2
        bet.save()
        self.assertEqual(100, user.current_portfolio_value)

    def test_get_avatar_url(self):
        """
        Get avatar URL
        """
        user = UserFactory()
        self.assertEqual('/static/img/blank-avatar.jpg', user.get_avatar_url())
        user2 = UserWithAvatarFactory(username='johnrambro')
        self.assertEqual('avatars/johnrambro.jpg', user2.get_avatar_url())
        os.remove('avatars/johnrambro.jpg')

    def test_reset_account_without_bonus(self):
        """
        Test reset account
        """
        user = UserFactory()
        user.reset_account()
        self.assertEqual({
            'user_id': 1,
            'total_cash': formatted(1000),
            'portfolio_value': formatted(0),
            'reputation': "100%",
        }, user.statistics_dict)

    def test_reset_account_with_bonus(self):
        """
        Test reset account
        """
        user = UserFactory()
        user.reset_account(0.1)
        self.assertEqual({
            'user_id': 1,
            'total_cash': formatted(1100),
            'portfolio_value': formatted(0),
            'reputation': "110%",
        }, user.statistics_dict)

    def test_get_newest_results(self):
        """
        Get newest results
        """
        users = UserFactory.create_batch(2)
        events = EventFactory.create_batch(5)
        BetFactory(user=users[0], event=events[0])
        bet2 = BetFactory(user=users[0], event=events[1])
        bet3 = BetFactory(user=users[0], event=events[2])
        bet4 = BetFactory(user=users[0], event=events[3])
        bet5 = BetFactory(user=users[1], event=events[4])
        events[1].outcome = Event.CANCELLED
        events[1].save()
        events[2].outcome = Event.FINISHED_YES
        events[2].save()
        events[3].outcome = Event.FINISHED_NO
        events[3].save()
        events[4].outcome = Event.FINISHED_YES
        events[4].save()
        bet2.is_new_resolved = True
        bet2.save()
        bet3.is_new_resolved = True
        bet3.save()
        bet4.is_new_resolved = True
        bet4.save()
        bet5.is_new_resolved = True
        bet5.save()
        self.assertEqual([bet2, bet3, bet4], list(users[0].get_newest_results()))
        self.assertEqual([bet5], list(users[1].get_newest_results()))


class UserProfileManagerTestCase(TestCase):
    """
    accounts/managers UserProfileManager
    """
    def test_return_new_user_object(self):
        """
        Return new user object
        """
        user = UserProfile.objects.return_new_user_object(
            username='j_smith',
            password='password9',
        )
        self.assertIsInstance(user, UserProfile)
        self.assertEqual('j_smith', user.username)
        self.assertTrue(user.check_password('password9'))

        with self.assertRaises(ValueError):
            UserProfile.objects.return_new_user_object(
                username=None,
            )

    def test_create_user(self):
        """
        Create user
        """
        user = UserProfile.objects.create_user(
            username='j_smith',
            email='j_smith@example.com',
            password='password9',
        )
        self.assertIsInstance(user, UserProfile)
        self.assertEqual('j_smith', user.username)
        self.assertTrue(user.check_password('password9'))
        self.assertTrue(user.is_active)
        self.assertEqual({
            'user_id': 1,
            'total_cash': formatted(config.STARTING_CASH),
            'portfolio_value': formatted(0),
            'reputation': '100%',
        }, user.statistics_dict)

        user2 = UserProfile.objects.create_user(
            username='j_smith',
            email='j_smith@example.com',
        )
        self.assertIsInstance(user2, HttpResponseForbidden)

    def test_create_superuser(self):
        """
        Create superuser
        """
        user = UserProfile.objects.create_superuser(
            username='j_smith',
            email='j_smith@example.com',
            password='password9',
        )
        self.assertIsInstance(user, UserProfile)
        self.assertEqual('j_smith', user.username)
        self.assertTrue(user.check_password('password9'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_active)
        self.assertEqual({
            'user_id': 1,
            'total_cash': formatted(0),
            'portfolio_value': formatted(0),
            'reputation': '100%',
        }, user.statistics_dict)

        user2 = UserProfile.objects.create_superuser(
            username='j_smith',
            email='j_smith@example.com',
        )
        self.assertIsInstance(user2, HttpResponseForbidden)

    def test_create_user_with_random_password(self):
        """
        Create user with random password
        """
        user, password = UserProfile.objects.create_user_with_random_password(
            username='j_smith',
        )
        self.assertTrue(user.check_password(password))

    def test_get_users(self):
        """
        Get users
        """
        user1 = UserFactory()
        UserFactory(is_deleted=True)
        UserFactory(is_active=False)

        users = UserProfile.objects.get_users()
        self.assertIsInstance(users[0], UserProfile)
        self.assertEqual(1, len(users))
        self.assertEqual([user1], list(users))

    def test_get_ranking_users(self):
        """
        Get ranking users
        """
        UserFactory()
        UserFactory()
        UserFactory(is_deleted=True)
        UserFactory(is_active=False)

        users = UserProfile.objects.get_ranking_users()
        self.assertEqual(0, len(users))
        self.assertEqual([], list(users))
        # TODO mock transaction

    def test_get_admins(self):
        """
        Get admins
        """
        UserFactory()
        UserFactory(is_admin=True)
        UserFactory(is_staff=True)
        user4 = AdminFactory()

        admins = UserProfile.objects.get_admins()
        self.assertIsInstance(admins[0], UserProfile)
        self.assertEqual(1, len(admins))
        self.assertEqual([user4], list(admins))

    def test_get_best_weekly(self):
        """
        Get best weekly
        """
        user1 = UserFactory(weekly_result=100)
        user2 = UserFactory(weekly_result=300)
        UserFactory()
        AdminFactory()

        users = UserProfile.objects.get_best_weekly()
        self.assertEqual(0, len(users))
        self.assertEqual([], list(users))
        # TODO mock transaction
        # self.assertIsInstance(users[0], UserProfile)
        # self.assertEqual(2, len(users))
        # self.assertEqual([user2, user1], list(users))

    def test_get_best_monthly(self):
        """
        Get best monthly
        """
        UserFactory()
        user2 = UserFactory(monthly_result=300)
        AdminFactory()
        user4 = UserFactory(monthly_result=100)

        users = UserProfile.objects.get_best_monthly()
        self.assertEqual(0, len(users))
        self.assertEqual([], list(users))
        # TODO mock transaction
        # self.assertIsInstance(users[0], UserProfile)
        # self.assertEqual(2, len(users))
        # self.assertEqual([user2, user4], list(users))

    def test_get_best_overall(self):
        """
        Get best overall
        """
        user1 = UserFactory()
        user2 = UserFactory(reputation=Decimal(300))
        AdminFactory()
        user4 = UserFactory(reputation=Decimal(50))

        users = UserProfile.objects.get_best_overall()
        self.assertEqual(0, len(users))
        self.assertEqual([], list(users))
        # TODO mock transaction
        # self.assertIsInstance(users[0], UserProfile)
        # self.assertEqual(3, len(users))
        # self.assertEqual([user2, user1, user4], list(users))

    def test_get_user_positions(self):
        """
        Get user positions
        """
        user1 = UserFactory(weekly_result=100)
        user2 = UserFactory(weekly_result=300, monthly_result=300, reputation=Decimal(300))
        user3 = AdminFactory()
        user4 = UserFactory(monthly_result=100, reputation=Decimal(50))

        # TODO mock
        self.assertEqual({
            'week_rank': '-',
            'month_rank': '-',
            'overall_rank': '-'
        }, UserProfile.objects.get_user_positions(user1))
        self.assertEqual({
            'week_rank': '-',
            'month_rank': '-',
            'overall_rank': '-'
        }, UserProfile.objects.get_user_positions(user2))
        self.assertEqual({
            'week_rank': '-',
            'month_rank': '-',
            'overall_rank': '-'
        }, UserProfile.objects.get_user_positions(user3))
        self.assertEqual({
            'week_rank': '-',
            'month_rank': '-',
            'overall_rank': '-'
        }, UserProfile.objects.get_user_positions(user4))
        # self.assertEqual({
        #     'week_rank': 2,
        #     'month_rank': '-',
        #     'overall_rank': 2
        # }, UserProfile.objects.get_user_positions(user1))
        # self.assertEqual({
        #     'week_rank': 1,
        #     'month_rank': 1,
        #     'overall_rank': 1
        # }, UserProfile.objects.get_user_positions(user2))
        # self.assertEqual({
        #     'week_rank': '-',
        #     'month_rank': '-',
        #     'overall_rank': '-'
        # }, UserProfile.objects.get_user_positions(user3))
        # self.assertEqual({
        #     'week_rank': '-',
        #     'month_rank': 2,
        #     'overall_rank': 3
        # }, UserProfile.objects.get_user_positions(user4))


class UserPipelineTestCase(TestCase):
    """
    accounts/pipeline
    """
    def test_save_profile(self):
        """
        Save profile
        """
        user = UserFactory()
        #  save_profile(user,


class UserTasksTestCase(TestCase):
    """
    accounts/tasks
    """
    def test_topup_accounts_task(self):
        """
        Topup
        """
        user = UserFactory()
        topup_accounts_task()
        user.refresh_from_db()
        self.assertEqual(config.DAILY_TOPUP, user.total_cash)
        # TODO mock and test exception

    @patch.object(UserProfile, 'topup_cash')
    @patch('accounts.tasks.logger')
    def test_topup_accounts_task_error(self, logger, topup_cash):
        UserFactory()
        topup_cash.side_effect = Exception()
        topup_accounts_task()
        logger.exception.assert_called_once()


    def test_update_portfolio_value(self):
        """
        Update portfolio_value
        """
        price = 90
        user = UserFactory()
        event = EventFactory(current_sell_for_price=price)
        BetFactory(user=user, event=event, has=1, outcome=True)

        self.assertEqual(0, user.portfolio_value)
        update_portfolio_value()
        user.refresh_from_db()
        # TODO FIXME
        # self.assertEqual(price, user.portfolio_value)

    def test_create_accounts_snapshot(self):
        user = UserFactory()
        create_accounts_snapshot()
        # TODO mock logger and create_snapshot()

    def test_update_users_classification(self):
        users = UserFactory.create_batch(6)
        update_users_classification()
        # TODO: mock reputation changes


class UserTemplatetagsTestCase(TestCase):
    """
    accounts/templatetags
    """
    def test_user_home(self):
        """
        User home
        """
        user = UserFactory()
        user_templatetag = user_home(user, 1000, True)
        self.assertEqual({
            'user': user,
            'reputation_change': 1000,
            'is_formatted': True
        }, user_templatetag)
        user_templatetag = user_home(user, -100)
        self.assertEqual({
            'user': user,
            'reputation_change': -100,
            'is_formatted': False
        }, user_templatetag)

    # TODO FIXME
    # def test_user_rank(self):
    #     """
    #     User rank
    #     """
    #     user = UserFactory()
    #     user_templatetag = user_rank(user)
    #     self.assertEqual({
    #         'profit': None,
    #         'user': user,
    #         'counter': 1,
    #     }, user_templatetag)
    #     user_templatetag_with_profit = user_rank(user, 10)
    #     self.assertEqual({
    #         'profit': 10,
    #         'user': user,
    #         'counter': 1,
    #     }, user_templatetag_with_profit)

    def test_get_reputation_history(self):
        """
        Get reputation history
        """
        # TODO

    def test_get_reputation_change(self):
        """
        Get reputation change
        """
        # TODO

    def test_last_week_reputation_change(self):
        """
        Get last week reputation change
        """
        # TODO

    def test_last_month_reputation_change(self):
        """
        Get last month reputation change
        """
        # TODO


class PolitikonUserTemplatetagsTestCase(TestCase):
    """
    politikon/templatetags
    """
    def test_startswith(self):
        """
        Startswith
        """
        start_path = reverse('accounts:rank')
        path = reverse('accounts:rank')
        self.assertTrue(startswith(path, start_path))


class UserUtilsTestCase(TestCase):
    """
    accounts/utils
    """
    def test_process_username(self):
        """
        Process username
        """
        username = process_username(u"zażółćgęśląjaźń")
        self.assertEqual('zazolcgeslajazn', username)
        UserFactory(username='zazolcgeslajazn')
        username2 = process_username(u"zażółćgęśląjaźń")
        self.assertNotEqual('zazolcgeslajazn', username2)
