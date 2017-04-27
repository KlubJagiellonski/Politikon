# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20170331_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='B',
            field=models.FloatField(default=10, verbose_name='sta\u0142a B'),
        ),
        migrations.AlterField(
            model_name='eventsnapshot',
            name='B',
            field=models.FloatField(default=10, verbose_name='sta\u0142a B'),
        ),
    ]
