# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=1024, verbose_name='username')),
                ('email', models.CharField(unique=True, max_length=1024, verbose_name='email')),
                ('avatarURL', models.CharField(default=b'', max_length=1024, verbose_name='avatar_url')),
                ('name', models.CharField(max_length=1024, blank=True)),
                ('is_admin', models.BooleanField(default=False, verbose_name='is an administrator')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is deleted')),
                ('is_authenticated', models.BooleanField(default=False, verbose_name='is authenticated')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('total_cash', models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 got\xf3wki')),
                ('total_given_cash', models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 przyznanej got\xf3wki w historii')),
                ('portfolio_value', models.IntegerField(default=0.0, verbose_name='warto\u015b\u0107 portfela')),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfileSnapshot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='stworzony dnia')),
                ('total_cash', models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 got\xf3wki')),
                ('total_given_cash', models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 przyznanej got\xf3wki w historii')),
                ('portfolio_value', models.IntegerField(default=0.0, verbose_name='warto\u015b\u0107 portfela')),
                ('snapshot_of', models.ForeignKey(related_name='snapshots', on_delete=django.db.models.deletion.PROTECT, verbose_name='dotyczy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'accounts_userprofile_snapshot',
                'verbose_name': 'user profile - snapshot',
                'verbose_name_plural': 'user profile - snapshoty',
            },
        ),
    ]
