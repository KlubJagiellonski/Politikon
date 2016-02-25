# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20160214_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='absolute_price_change',
            field=models.IntegerField(default=0, verbose_name='zmiana ceny (warto\u015b\u0107                                                 absolutna)', db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='current_buy_against_price',
            field=models.IntegerField(default=50.0, verbose_name='cena nabycia akcji                                                     zdarzenia przeciwnego'),
        ),
        migrations.AlterField(
            model_name='event',
            name='current_buy_for_price',
            field=models.IntegerField(default=50.0, verbose_name='cena nabycia akcji                                                 zdarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='current_sell_against_price',
            field=models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji                                                      zdarzenia przeciwnego'),
        ),
        migrations.AlterField(
            model_name='event',
            name='current_sell_for_price',
            field=models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji                                                  zdarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='estimated_end_date',
            field=models.DateTimeField(verbose_name='przewidywana data                                               rozstrzygni\u0119cia'),
        ),
        migrations.AlterField(
            model_name='eventsnapshot',
            name='current_buy_against_price',
            field=models.IntegerField(default=50.0, verbose_name='cena nabycia akcji                                                     zdarzenia przeciwnego'),
        ),
        migrations.AlterField(
            model_name='eventsnapshot',
            name='current_buy_for_price',
            field=models.IntegerField(default=50.0, verbose_name='cena nabycia akcji                                                 zdarzenia'),
        ),
        migrations.AlterField(
            model_name='eventsnapshot',
            name='current_sell_against_price',
            field=models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji                                                      zdarzenia przeciwnego'),
        ),
        migrations.AlterField(
            model_name='eventsnapshot',
            name='current_sell_for_price',
            field=models.IntegerField(default=50.0, verbose_name='cena sprzeda\u017cy akcji                                                  zdarzenia'),
        ),
    ]
