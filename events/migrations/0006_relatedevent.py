# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_outcome_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(related_query_name=b'this_event', related_name='these_events', to='events.Event', null=True)),
                ('related', models.ForeignKey(related_query_name=b'related', related_name='relates', to='events.Event', null=True)),
            ],
        ),
    ]
