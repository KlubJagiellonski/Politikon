# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160219_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatarURL',
        ),
    ]
