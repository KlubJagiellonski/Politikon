# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0016_auto_20160625_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolutionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('outcome', models.IntegerField(null=True, verbose_name='rozwi\u0105zanie wydarzenia', choices=[(1, 'rozwi\u0105zanie na TAK'), (2, 'rozwi\u0105zanie na NIE')])),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='resolved_by',
        ),
        migrations.AddField(
            model_name='event',
            name='vote_no_count',
            field=models.PositiveIntegerField(default=0, verbose_name='g\u0142os\xf3w na nie'),
        ),
        migrations.AddField(
            model_name='event',
            name='vote_yes_count',
            field=models.PositiveIntegerField(default=0, verbose_name='g\u0142os\xf3w na tak'),
        ),
        migrations.AddField(
            model_name='solutionvote',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='solutionvote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='solutionvote',
            unique_together=set([('user', 'event')]),
        ),
    ]
