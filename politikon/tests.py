# -*- coding: utf-8 -*-
"""
Test accounts module
"""
from django.test import TestCase

from .templatetags.format import formatted, toLower


class UserTemplatetagTestCase(TestCase):
    """
    accounts/templatetags
    """
    def test_formatted(self):
        """
        formatted templatetag
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

    def test_toLower(self):
        """
        toLower
        """
        text = "LOREM IPSUM"
        self.assertEqual("lOREM IPSUM", toLower(text))

        text = "lorem ipsum"
        self.assertEqual("lorem ipsum", toLower(text))

        text = ""
        self.assertEqual("", toLower(text))
