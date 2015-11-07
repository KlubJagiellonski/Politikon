# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='event',
            field=models.ForeignKey(related_query_name=b'bet', related_name='bets', to='events.Event'),
        ),
        migrations.AlterField(
            model_name='bet',
            name='outcome',
            field=models.BooleanField(verbose_name='zak\u0142ad na TAK', choices=[(True, 'udzia\u0142y na TAK'), (False, 'udzia\u0142y na NIE')]),
        ),
        migrations.AlterField(
            model_name='bet',
            name='user',
            field=models.ForeignKey(related_query_name=b'bet', related_name='bets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='event',
            field=models.ForeignKey(related_query_name=b'transaction', related_name='transactions', to='events.Event', null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.PositiveIntegerField(default=1, verbose_name=b'rodzaj transakcji', choices=[(1, 'zakup udzia\u0142\xf3w na TAK'), (2, 'sprzeda\u017c udzia\u0142\xf3w na TAK'), (3, 'zakup udzia\u0142\xf3w na NIE'), (4, 'sprzeda\u017c udzia\u0142\xf3w na NIE'), (5, 'zwrot po anulowaniu wydarzenia'), (6, 'wygrana po rozstrzygni\u0119ciu wydarzenia'), (7, 'do\u0142adowanie konta przez aplikacj\u0119')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(related_query_name=b'transaction', related_name='transactions', to=settings.AUTH_USER_MODEL),
        ),
    ]
