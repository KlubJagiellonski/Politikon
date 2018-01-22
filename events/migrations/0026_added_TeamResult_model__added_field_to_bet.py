# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20170531_0031'),
        ('events', '0025_auto_20170601_0239'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('elo', models.IntegerField(null=True, verbose_name='ranking', blank=True)),
                ('initial_elo', models.IntegerField(default=1400, verbose_name='pocz\u0105tkowy ranking')),
                ('rewarded_total', models.IntegerField(default=0, verbose_name='nagroda za wynik')),
                ('bets_count', models.PositiveIntegerField(verbose_name='liczba zak\u0142ad\xf3w')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='utworzono')),
                ('event', models.ForeignKey(related_query_name=b'team_result', related_name='team_results', to='events.Event')),
                ('prev_result', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='events.TeamResult')),
                ('team', models.ForeignKey(related_query_name=b'result', related_name='results', to='accounts.Team')),
            ],
            options={
                'verbose_name': 'rezultat dru\u017cyny',
                'verbose_name_plural': 'rezultaty dru\u017cyn',
            },
        ),
        migrations.AddField(
            model_name='bet',
            name='team_result',
            field=models.ForeignKey(related_query_name=b'bet', related_name='bets', to='events.TeamResult', null=True),
        ),
    ]
