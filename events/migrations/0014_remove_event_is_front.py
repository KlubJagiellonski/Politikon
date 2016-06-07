# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20160607_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_front',
        ),
    ]
