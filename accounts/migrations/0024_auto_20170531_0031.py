# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20170517_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='name')),
                ('avatar', models.ImageField(null=True, upload_to=accounts.models.get_team_avatar_path, blank=True)),
                ('avg_reputation', models.DecimalField(null=True, verbose_name='reputation', max_digits=12, decimal_places=2, blank=True)),
                ('avg_total_cash', models.DecimalField(null=True, verbose_name='total cash', max_digits=12, decimal_places=2, blank=True)),
                ('avg_portfolio_value', models.DecimalField(null=True, verbose_name='portfolio value', max_digits=12, decimal_places=2, blank=True)),
                ('avg_weekly_result', models.DecimalField(null=True, verbose_name='weekly result', max_digits=7, decimal_places=2, blank=True)),
                ('avg_monthly_result', models.DecimalField(null=True, verbose_name='monthly result', max_digits=7, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ['avg_reputation'],
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='team',
            field=models.ForeignKey(verbose_name='team', blank=True, to='accounts.Team', null=True),
        ),
    ]
