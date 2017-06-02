# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20170523_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='tytu\u0142 wydarzenia')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug url')),
            ],
            options={
                'verbose_name': 'kategoria',
                'verbose_name_plural': 'kategorie',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='categories',
            field=models.ManyToManyField(to='events.EventCategory', verbose_name='kategorie', blank=True),
        ),
    ]
