# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('outcome', models.BooleanField(verbose_name='zak\u0142ad na TAK', choices=[(True, b'udzia\xc5\x82y na TAK'), (False, b'udzia\xc5\x82y na NIE')])),
                ('has', models.PositiveIntegerField(default=0, verbose_name='posiadane zak\u0142ady')),
                ('bought', models.PositiveIntegerField(default=0, verbose_name='kupione\xa0zak\u0142ady')),
                ('sold', models.PositiveIntegerField(default=0, verbose_name='sprzedane zak\u0142ady')),
                ('bought_avg_price', models.FloatField(default=0, verbose_name='kupione po \u015bredniej cenie')),
                ('sold_avg_price', models.FloatField(default=0, verbose_name='sprzedane po \u015bredniej cenie')),
                ('rewarded_total', models.IntegerField(default=0, verbose_name='nagroda za wynik')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(verbose_name='tytu\u0142 wydarzenia')),
                ('short_title', models.TextField(verbose_name='tytu\u0142 promocyjny wydarzenia')),
                ('title_fb_yes', models.TextField(verbose_name='tytu\u0142 na TAK obiektu FB')),
                ('title_fb_no', models.TextField(verbose_name='tytu\u0142 na NIE obiektu FB')),
                ('description', models.TextField(default=b'', verbose_name='pe\u0142ny opis wydarzenia')),
                ('small_image', models.ImageField(upload_to=b'events_small', null=True, verbose_name='ma\u0142y obrazek 340x250')),
                ('big_image', models.ImageField(upload_to=b'events_big', null=True, verbose_name='du\u017cy obrazek 1250x510')),
                ('is_featured', models.BooleanField(default=False, verbose_name='featured')),
                ('is_front', models.BooleanField(default=False, verbose_name='front')),
                ('outcome', models.PositiveIntegerField(default=1, verbose_name='rozstrzygni\u0119cie', choices=[(1, 'w trakcie'), (2, 'anulowane'), (3, 'rozstrzygni\u0119te na TAK'), (4, 'rozstrzygni\u0119te na NIE')])),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('estimated_end_date', models.DateTimeField(verbose_name='przewidywana data rozstrzygni\u0119cia')),
                ('end_date', models.DateTimeField(null=True, verbose_name='data rozstrzygni\u0119cia')),
                ('current_buy_for_price', models.IntegerField(default=50.0, verbose_name='cena nabycia akcji zdarzenia')),
                ('current_buy_against_price', models.IntegerField(default=50.0, verbose_name='cena nabycia akcji zdarzenia przeciwnego')),
                ('current_sell_for_price', models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji zdarzenia')),
                ('current_sell_against_price', models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji zdarzenia przeciwnego')),
                ('last_transaction_date', models.DateTimeField(null=True, verbose_name='data ostatniej transakcji')),
                ('Q_for', models.IntegerField(default=0, verbose_name='zak\u0142ad\xf3w na TAK')),
                ('Q_against', models.IntegerField(default=0, verbose_name='zak\u0142ad\xf3w na NIE')),
                ('turnover', models.IntegerField(default=0, verbose_name='obr\xf3t', db_index=True)),
                ('absolute_price_change', models.IntegerField(default=0, verbose_name='zmiana ceny (warto\u015b\u0107 absolutna)', db_index=True)),
                ('price_change', models.IntegerField(default=0, verbose_name='zmiana ceny')),
                ('B', models.FloatField(default=5, verbose_name='sta\u0142a B')),
            ],
        ),
        migrations.CreateModel(
            name='EventSnapshot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='stworzony dnia')),
                ('current_buy_for_price', models.IntegerField(default=50.0, verbose_name='cena nabycia akcji zdarzenia')),
                ('current_buy_against_price', models.IntegerField(default=50.0, verbose_name='cena nabycia akcji zdarzenia przeciwnego')),
                ('current_sell_for_price', models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji zdarzenia')),
                ('current_sell_against_price', models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji zdarzenia przeciwnego')),
                ('Q_for', models.IntegerField(default=0, verbose_name='zak\u0142ad\xf3w na TAK')),
                ('Q_against', models.IntegerField(default=0, verbose_name='zak\u0142ad\xf3w na NIE')),
                ('B', models.FloatField(default=5, verbose_name='sta\u0142a B')),
                ('snapshot_of', models.ForeignKey(related_name='snapshots', on_delete=django.db.models.deletion.PROTECT, verbose_name='dotyczy', to='events.Event')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'events_event_snapshot',
                'verbose_name': 'event - snapshot',
                'verbose_name_plural': 'event - snapshoty',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveIntegerField(default=1, verbose_name=b'rodzaj transakcji', choices=[(1, b'zakup udzia\xc5\x82\xc3\xb3w na TAK'), (2, b'sprzeda\xc5\xbc udzia\xc5\x82\xc3\xb3w na TAK'), (3, b'zakup udzia\xc5\x82\xc3\xb3w na NIE'), (4, b'sprzeda\xc5\xbc udzia\xc5\x82\xc3\xb3w na NIE'), (5, b'zwrot po anulowaniu wydarzenia'), (6, b'wygrana po rozstrzygni\xc4\x99ciu wydarzenia'), (7, b'do\xc5\x82adowanie konta przez aplikacj\xc4\x99')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='ilo\u015b\u0107')),
                ('price', models.IntegerField(default=0, verbose_name='cena jednostkowa')),
                ('event', models.ForeignKey(to='events.Event', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bet',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='bet',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
