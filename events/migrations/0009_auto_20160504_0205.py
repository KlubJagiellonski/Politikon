# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.AddField(
            model_name='event',
            name='resolved_by',
            field=models.ForeignKey(verbose_name='rozstrzygni\u0119te przez', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_fb_no',
            field=models.TextField(default=b'', verbose_name='tytu\u0142 na NIE obiektu FB'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title_fb_yes',
            field=models.TextField(default=b'', verbose_name='tytu\u0142 na TAK obiektu FB'),
        ),
    ]
