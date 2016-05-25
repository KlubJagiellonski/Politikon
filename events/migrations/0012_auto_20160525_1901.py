# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0011_auto_20160518_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(related_name='created_by', verbose_name='utworzone przez', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='data rozstrzygni\u0119cia', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='resolved_by',
            field=models.ForeignKey(related_name='resolved_by', verbose_name='rozstrzygni\u0119te przez', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
