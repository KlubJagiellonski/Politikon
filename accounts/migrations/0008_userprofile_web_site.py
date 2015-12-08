# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151107_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='web_site',
            field=models.CharField(default=b'', max_length=255, verbose_name='strona www'),
        ),
    ]
