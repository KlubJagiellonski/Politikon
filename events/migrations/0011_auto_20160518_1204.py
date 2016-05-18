# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20160516_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relatedevent',
            name='event',
        ),
        migrations.RemoveField(
            model_name='relatedevent',
            name='related',
        ),
        migrations.DeleteModel(
            name='RelatedEvent',
        ),
    ]
