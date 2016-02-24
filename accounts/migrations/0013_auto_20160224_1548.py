# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20160223_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='web_site',
            field=models.URLField(default=b'', max_length=255, verbose_name='strona www'),
        ),
    ]
