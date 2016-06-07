# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20160525_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='outcome_reason',
            field=models.TextField(default=b'', verbose_name='uzasadnienie wyniku', blank=True),
        ),
    ]
