# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_bet_is_new_resolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='outcome_reason',
            field=models.TextField(default=b'', verbose_name='uzazadnienie wyniku'),
        ),
    ]
