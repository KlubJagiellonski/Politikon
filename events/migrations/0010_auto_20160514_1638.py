# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20160504_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='big_image',
            field=models.ImageField(upload_to=b'events_big', null=True, verbose_name='du\u017cy obrazek 1250x510', blank=True),
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
