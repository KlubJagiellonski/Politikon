# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20170427_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
