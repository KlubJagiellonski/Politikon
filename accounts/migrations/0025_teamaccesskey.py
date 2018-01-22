# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20170531_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamAccessKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(default=accounts.utils.generate_random_string, max_length=60)),
                ('team', models.ForeignKey(verbose_name='team', to='accounts.Team')),
            ],
            options={
                'verbose_name': 'team access key',
                'verbose_name_plural': 'team access keys',
            },
        ),
    ]
