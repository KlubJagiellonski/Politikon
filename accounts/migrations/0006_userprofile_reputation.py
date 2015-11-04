# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151103_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='reputation',
            field=models.DecimalField(default=0, verbose_name='reputation', max_digits=12, decimal_places=2),
        ),
    ]
