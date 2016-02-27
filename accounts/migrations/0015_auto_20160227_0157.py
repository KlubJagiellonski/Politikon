# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20160224_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='monthly_result',
            field=models.IntegerField(null=True, verbose_name='wynik miesi\u0119czny', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='weekly_result',
            field=models.IntegerField(null=True, verbose_name='wynik tygodniowy', blank=True),
        ),
    ]
