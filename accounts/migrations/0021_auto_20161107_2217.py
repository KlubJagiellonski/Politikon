# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_last_transaction(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    Transaction = apps.get_model('events', 'Transaction')

    BUY_YES, SELL_YES, BUY_NO, SELL_NO, EVENT_CANCELLED_REFUND, EVENT_CANCELLED_DEBIT, \
    EVENT_WON_PRIZE, TOPPED_UP_BY_APP, BONUS = range(1, 10)

    BUY_SELL_TYPES = (
        BUY_YES,
        SELL_YES,
        BUY_NO,
        SELL_NO,
    )
    for user in UserProfile.objects.all():
        transactions = Transaction.objects.filter(type__in=BUY_SELL_TYPES, user=user).order_by('-date')
        if len(transactions):
            user.last_transaction = transactions[0].date
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_userprofile_last_transaction'),
        ('events', '0018_auto_20161004_2009')
    ]

    operations = [
        migrations.RunPython(set_last_transaction),
    ]
