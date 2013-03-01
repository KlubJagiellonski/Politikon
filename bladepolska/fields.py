# coding: utf-8

from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.fields import DecimalField


class LenientDecimalField(DecimalField):
    def __init__(self, allowed_currency_symbols=[], *args, **kwargs):
        self.allowed_currency_symbols = allowed_currency_symbols

        super(LenientDecimalField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        # strip the currency symbols
        for symbol in self.allowed_currency_symbols:
            value = value.replace(symbol, '')

        if value.startswith("."):
            value = u"0%s" % value

        return super(LenientDecimalField, self).to_python(value)

    def bound_data(self, data, initial):
        try:
            return unicode(self.to_python(data))
        except:
            return unicode(data)
