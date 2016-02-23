# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_userprofile_avatarurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=255, null=True, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='total_given_cash',
            field=models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 przyznanej got\xf3wki w                                            historii'),
        ),
        migrations.AlterField(
            model_name='userprofilesnapshot',
            name='total_given_cash',
            field=models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 przyznanej got\xf3wki w                                            historii'),
        ),
    ]
