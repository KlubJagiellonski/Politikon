# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151013_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default=b'', max_length=255, verbose_name='kr\xf3tki opis'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='facebook_user',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='facebook URL', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='facebook_user_id',
            field=models.IntegerField(default=None, null=True, verbose_name='facebook ID', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter_user',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='twitter URL', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter_user_id',
            field=models.IntegerField(default=None, null=True, verbose_name='twitter ID', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatarURL',
            field=models.CharField(default=b'', max_length=255, verbose_name='avatar_url'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=255, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(unique=True, max_length=100, verbose_name='username'),
        ),
    ]
