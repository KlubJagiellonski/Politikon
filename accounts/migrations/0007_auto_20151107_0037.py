# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile_reputation'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_vip',
            field=models.BooleanField(default=False, verbose_name='VIP'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='unused_reput',
            field=models.IntegerField(default=0, verbose_name='wolne reputy'),
        ),
    ]
