# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20160224_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='unused_reput',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='reputation',
            field=models.DecimalField(default=100, verbose_name='reputation', max_digits=12, decimal_places=2),
        ),
    ]
