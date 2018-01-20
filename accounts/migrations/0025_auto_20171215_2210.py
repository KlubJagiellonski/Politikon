# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20170531_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.CharField(verbose_name='krótki opis', max_length=255, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='web_site',
            field=models.URLField(verbose_name='strona www', max_length=255, default=''),
        ),
    ]
