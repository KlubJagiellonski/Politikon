# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20170321_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='opublikowano'),
        ),
    ]
