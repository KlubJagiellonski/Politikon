# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20160824_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='vote_cancel_count',
            field=models.PositiveIntegerField(default=0, verbose_name='g\u0142os\xf3w na anuluj'),
        ),
        migrations.AlterField(
            model_name='solutionvote',
            name='outcome',
            field=models.IntegerField(null=True, verbose_name='rozwi\u0105zanie wydarzenia', choices=[(1, 'rozwi\u0105zanie na TAK'), (2, 'rozwi\u0105zanie na NIE'), (3, 'anulowanie wydarzenia')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.PositiveIntegerField(default=1, verbose_name=b'rodzaj transakcji', choices=[(1, 'zakup udzia\u0142\xf3w na TAK'), (2, 'sprzeda\u017c udzia\u0142\xf3w na TAK'), (3, 'zakup udzia\u0142\xf3w na NIE'), (4, 'sprzeda\u017c udzia\u0142\xf3w na NIE'), (5, 'zwrot po anulowaniu wydarzenia'), (6, 'obci\u0105\u017cenie konta po anulowaniu wydarzenia'), (7, 'wygrana po rozstrzygni\u0119ciu wydarzenia'), (8, 'do\u0142adowanie konta przez aplikacj\u0119'), (9, 'bonus')]),
        ),
    ]
