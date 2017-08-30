# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20170602_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extracontent',
            options={'verbose_name': 'extra content', 'verbose_name_plural': 'extra contents'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': 'page', 'verbose_name_plural': 'pages'},
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(verbose_name='slug url'),
        ),
    ]
