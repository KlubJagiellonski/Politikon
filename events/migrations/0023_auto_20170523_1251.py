# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20170521_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='estimated_end_date',
            field=models.DateTimeField(null=True, verbose_name='przewidywana data rozstrzygni\u0119cia'),
        ),
    ]
