# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20161004_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='szkic'),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='wyr\xf3\u017cniony'),
        ),
        migrations.AlterField(
            model_name='event',
            name='short_title',
            field=models.CharField(default=b'', max_length=255, verbose_name='tytu\u0142 promocyjny wydarzenia', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=255, verbose_name='tytu\u0142 wydarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_fb_no',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='tytu\u0142 na NIE obiektu FB', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_fb_yes',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='tytu\u0142 na TAK obiektu FB', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='twitter_tag',
            field=models.CharField(default=b'', validators=[django.core.validators.RegexValidator(regex=b'^([^\\s]+)$', message='Tag twittera nie mo\u017ce zawiera\u0107 spacji', code=b'invalid_twitter_tag')], max_length=32, blank=True, null=True, verbose_name='tag twittera'),
        ),
    ]
