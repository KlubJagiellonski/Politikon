# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20160202_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='is_new_resolved',
            field=models.BooleanField(default=False, verbose_name='ostatnio rozstrzygni\u0119te'),
        ),
    ]
