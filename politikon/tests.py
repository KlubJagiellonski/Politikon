# -*- coding: utf-8 -*-
"""
Test accounts module
"""
from django.test import TestCase

from .templatetags.format import formatted


class UserTemplatetagTestCase(TestCase):
    """
    accounts/templatetags
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
