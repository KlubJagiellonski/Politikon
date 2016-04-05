# -*- coding: utf-8 -*-
"""
Test accounts module
"""
from decimal import Decimal

from django.http import HttpResponseForbidden
from django.test import TestCase

from .factories import UserFactory, BaBroracusFactory, BroHardFactory, \
    AdminFactory
from .managers import UserProfileManager
from .models import UserProfile, get_image_path
from .utils import process_username
from constance import config
from events.templatetags.format import formatted


class UserProfileModelTestCase(TestCase):
    """
    Test method for user object
    """
    def test_user_creation(self):
        """
        Create user and check his attributes
        """
        user = UserFactory()

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
            'reputation': '0%',
        }, user.statistics_dict)
        self.assertEqual(0, user.current_portfolio_value)

    def test_get_image_path(self):
        """
        Get image path
        """
        user = UserFactory()

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

        url = user.get_absolute_url()
        self.assertEqual('/accounts/1/', url)

        url = user.get_avatar_url()
        self.assertEqual('/static/img/blank-avatar.jpg', url)

        url = user.get_twitter_url()
        self.assertEqual('https://twitter.com/jsmith', url)

        url = user.get_facebook_url()
        self.assertEqual('https://www.facebook.com/facesmith', url)

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

    def test_playing_user(self):
        """
        Create user and play
        """
        user = UserFactory()


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
            user2 = UserProfile.objects.return_new_user_object(
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
        self.assertFalse(user.is_active)
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
        user2 = BaBroracusFactory(is_deleted=True)
        user3 = BroHardFactory(is_active=False)

        users = UserProfile.objects.get_users()
        self.assertIsInstance(users[0], UserProfile)
        self.assertEqual(1, len(users))
        self.assertEqual([user1], list(users))

    def test_get_admins(self):
        """
        Get admins
        """
        user1 = UserFactory()
        user2 = BaBroracusFactory(is_admin=True)
        user3 = BroHardFactory(is_staff=True)
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
        user2 = BaBroracusFactory(weekly_result=300)
        user3 = BroHardFactory()
        user4 = AdminFactory()

        users = UserProfile.objects.get_best_weekly()
        self.assertIsInstance(users[0], UserProfile)
        self.assertEqual(2, len(users))
        self.assertEqual([user2, user1], list(users))

    def test_get_best_monthly(self):
        """
        Get best monthly
        """
        user1 = UserFactory()
        user2 = BaBroracusFactory(monthly_result=300)
        user3 = AdminFactory()
        user4 = BroHardFactory(monthly_result=100)

        users = UserProfile.objects.get_best_monthly()
        self.assertIsInstance(users[0], UserProfile)
        self.assertEqual(2, len(users))
        self.assertEqual([user2, user4], list(users))

    def test_get_best_overall(self):
        """
        Get best overall
        """
        user1 = UserFactory()
        user2 = BaBroracusFactory(reputation=Decimal(300))
        user3 = AdminFactory()
        user4 = BroHardFactory(reputation=Decimal(50))

        users = UserProfile.objects.get_best_overall()
        self.assertIsInstance(users[0], UserProfile)
        self.assertEqual(3, len(users))
        self.assertEqual([user2, user1, user4], list(users))

    def test_get_user_positions(self):
        """
        Get user positions
        """
        user1 = UserFactory(weekly_result=100)
        user2 = BaBroracusFactory(weekly_result=300, monthly_result=300,
                                  reputation=Decimal(300))
        user3 = AdminFactory()
        user4 = BroHardFactory(monthly_result=100, reputation=Decimal(50))

        self.assertEqual({
            'week_rank': 2,
            'month_rank': '-',
            'overall_rank': 2
        }, UserProfile.objects.get_user_positions(user1))
        self.assertEqual({
            'week_rank': 1,
            'month_rank': 1,
            'overall_rank': 1
        }, UserProfile.objects.get_user_positions(user2))
        self.assertEqual({
            'week_rank': '-',
            'month_rank': '-',
            'overall_rank': '-'
        }, UserProfile.objects.get_user_positions(user3))
        self.assertEqual({
            'week_rank': '-',
            'month_rank': 2,
            'overall_rank': 3
        }, UserProfile.objects.get_user_positions(user4))


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
