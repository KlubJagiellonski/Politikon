# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20160420_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 17, 10, 59, 14, 617472), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]
