# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20161107_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='monthly_result',
            field=models.DecimalField(null=True, verbose_name='wynik miesi\u0119czny', max_digits=7, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weekly_result',
            field=models.DecimalField(null=True, verbose_name='wynik tygodniowy', max_digits=7, decimal_places=2, blank=True),
        ),
    ]
