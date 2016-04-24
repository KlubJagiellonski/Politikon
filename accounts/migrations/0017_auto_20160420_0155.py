# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20160408_2259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'u\u017cytkownik', 'verbose_name_plural': 'u\u017cytkownicy'},
        ),
        migrations.AlterModelOptions(
            name='userprofilesnapshot',
            options={'ordering': ['-created_at'], 'verbose_name': 'u\u017cytkownik - snapshot', 'verbose_name_plural': 'u\u017cytkownik - snapshoty'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_visit',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='total_given_cash',
            field=models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 przyznanej got\xf3wki w historii'),
        ),
        migrations.AlterField(
            model_name='userprofilesnapshot',
            name='total_given_cash',
            field=models.IntegerField(default=0.0, verbose_name='ilo\u015b\u0107 przyznanej got\xf3wki w historii'),
        ),
    ]
