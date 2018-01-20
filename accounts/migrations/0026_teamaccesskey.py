# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20171215_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamAccessKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('value', models.CharField(max_length=60, default=accounts.utils.generate_random_string)),
                ('team', models.ForeignKey(verbose_name='team', to='accounts.Team')),
            ],
            options={
                'verbose_name': 'team access key',
                'verbose_name_plural': 'team access keys',
            },
        ),
    ]
