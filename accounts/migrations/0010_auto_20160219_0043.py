# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_user_id',
            field=models.BigIntegerField(default=None, null=True, verbose_name='facebook ID', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twitter_user_id',
            field=models.BigIntegerField(default=None, null=True, verbose_name='twitter ID', blank=True),
        ),
    ]
