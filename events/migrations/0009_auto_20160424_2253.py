# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20160330_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bet',
            options={'verbose_name': 'zak\u0142ad', 'verbose_name_plural': 'zak\u0142ady'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'wydarzenie', 'verbose_name_plural': 'wydarzenia'},
        ),
        migrations.AlterModelOptions(
            name='eventsnapshot',
            options={'ordering': ['-created_at'], 'verbose_name': 'wydarzenie - snapshot', 'verbose_name_plural': 'wydarzenie - snapshoty'},
        ),
        migrations.AlterModelOptions(
            name='relatedevent',
            options={'verbose_name': 'powi\u0105zane wydarzenie', 'verbose_name_plural': 'powi\u0105zane wydarzenia'},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date'], 'verbose_name': 'transakcja', 'verbose_name_plural': 'transakcje'},
        ),
        migrations.AlterField(
            model_name='event',
            name='big_image',
            field=models.ImageField(upload_to=b'events_big', null=True, verbose_name='du\u017cy obrazek 1250x510', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='short_title',
            field=models.TextField(default=b'', verbose_name='tytu\u0142 promocyjny wydarzenia', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='small_image',
            field=models.ImageField(upload_to=b'events_small', null=True, verbose_name='ma\u0142y obrazek 340x250', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_fb_no',
            field=models.TextField(default=b'', verbose_name='tytu\u0142 na NIE obiektu FB', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_fb_yes',
            field=models.TextField(default=b'', verbose_name='tytu\u0142 na TAK obiektu FB', blank=True),
        ),
    ]
