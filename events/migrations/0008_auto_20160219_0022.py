# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20160214_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='estimated_end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 26, 0, 22, 33, 714038), verbose_name='przewidywana data rozstrzygni\u0119cia'),
        ),
    ]
