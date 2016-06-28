# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20160615_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='big_image',
            field=imagekit.models.fields.ProcessedImageField(help_text='du\u017cy obrazek 1250x510', null=True, upload_to=b'events_big'),
        ),
        migrations.AlterField(
            model_name='event',
            name='small_image',
            field=imagekit.models.fields.ProcessedImageField(help_text='ma\u0142y obrazek 340x250', null=True, upload_to=b'events_small'),
        ),
        migrations.AlterField(
            model_name='event',
            name='twitter_tag',
            field=models.CharField(max_length=32, null=True, verbose_name='tag twittera', validators=[django.core.validators.RegexValidator(regex=b'^([^\\s]+)$', message='Tag twittera nie mo\u017ce zawiera\u0107 spacji', code=b'invalid_twitter_tag')]),
        ),
    ]
