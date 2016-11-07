# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20160518_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_transaction',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
