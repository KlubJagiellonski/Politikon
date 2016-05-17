# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_userprofile_active_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='active_date',
            new_name='reset_date',
        ),
    ]
