# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20170427_1932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelOptions(
            name='userprofilesnapshot',
            options={'ordering': ['-created_at'], 'verbose_name': 'user - snapshot', 'verbose_name_plural': 'user - snapshoty'},
        ),
    ]
