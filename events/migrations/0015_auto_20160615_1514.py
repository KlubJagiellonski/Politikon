# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_remove_event_is_front'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='twitter_tag',
            field=models.CharField(max_length=32, null=True, verbose_name='tag twittera', validators=[django.core.validators.RegexValidator(regex=b'^([^\\s]+)$', message=b'Bez spacji', code=b'invalid_twitter_tag')]),
        ),
    ]
