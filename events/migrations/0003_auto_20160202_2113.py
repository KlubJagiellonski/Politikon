# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151107_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='is_new_resolved',
            field=models.BooleanField(default=False, verbose_name='ostatnio rozstrzygni\u0119te'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'data'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.PositiveIntegerField(default=1, verbose_name=b'rodzaj transakcji', choices=[(1, 'zakup udzia\u0142\xf3w na TAK'), (2, 'sprzeda\u017c udzia\u0142\xf3w na TAK'), (3, 'zakup udzia\u0142\xf3w na NIE'), (4, 'sprzeda\u017c udzia\u0142\xf3w na NIE'), (5, 'zwrot po anulowaniu wydarzenia'), (6, 'obci\u0105\u017cenie konta po anulowaniu wydarzenia'), (7, 'wygrana po rozstrzygni\u0119ciu wydarzenia'), (8, 'do\u0142adowanie konta przez aplikacj\u0119')]),
        ),
    ]
