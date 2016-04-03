"""
Test accounts module
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .managers import UserProfileManager
from .models import UserProfile
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
        user = UserProfile.objects.create(
            username='johnsmith',
            name='John Smith',
        )

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

    def test_user_urls(self):
        """
        Check is urls are valid
        """
        user = UserProfile.objects.create(
            username='johnsmith',
            name='John Smith',
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
        j_smith = UserProfile.objects.create(
            username='johnsmith',
            name='John Smith',
        )

        url = j_smith.get_facebook_url()
        self.assertIsNone(url)

        url = j_smith.get_twitter_url()
        self.assertIsNone(url)

        j_smith.twitter_user = 'jsmith'
        j_smith.save()

        url = j_smith.get_twitter_url()
        self.assertEqual('https://twitter.com/jsmith', url)

    def test_playing_user(self):
        """
        Create user and play
        """
        user = UserProfile.objects.create(
            username='johnsmith',
            name='John Smith',
        )


class UserProfileManagerTestCase(TestCase):
    """
    accounts/managers UserProfileManager
    """
    def test_create_user(self):
        """
        Create user
        """
        UserProfile.objects.create_user(
            username='j_smith',
            email='j_smith@example.com',
            password='password9',
        )
        j_smith = UserProfile.objects.all()[0]
        self.assertIsInstance(j_smith, UserProfile)
        self.assertEqual('j_smith', j_smith.username)


