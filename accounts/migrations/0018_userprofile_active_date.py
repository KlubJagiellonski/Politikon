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
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 1, 0, 0), verbose_name='data ostatniej aktywacji', auto_now_add=True),
            preserve_default=False,
        ),
    ]
