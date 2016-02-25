"""
Test accounts module
"""
from decimal import Decimal

from django.test import TestCase

from django.contrib.auth.models import User
from .managers import UserProfileManager
from .models import UserProfile


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

        self.assertEqual('John Smith', user.name)
        self.assertEqual('John Smith', user.get_short_name())
        self.assertEqual(False, user.is_vip)
        self.assertEqual('John Smith (johnsmith)', user.get_full_name())
        user.calculate_reputation()
        self.assertEqual(Decimal(0), user.reputation)
        self.assertEqual(False, user.is_superuser)

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


