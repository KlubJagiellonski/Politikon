# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20160219_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='estimated_end_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 26, 0, 43, 1, 543726), verbose_name='przewidywana data rozstrzygni\u0119cia'),
        ),
    ]
