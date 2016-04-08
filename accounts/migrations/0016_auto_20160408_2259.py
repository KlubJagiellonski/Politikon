# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20160227_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='reputation',
            field=models.DecimalField(default=100, null=True, verbose_name='reputation', max_digits=12, decimal_places=2),
        ),
    ]
