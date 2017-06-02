# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    EventCategory = apps.get_model("events", "EventCategory")
    db_alias = schema_editor.connection.alias
    EventCategory.objects.using(db_alias).bulk_create([
        EventCategory(name=u"polityka krajowa", slug="polityka-krajowa"),
        EventCategory(name=u"polityka międzynarodowa", slug="polityka-miedzynarodowa"),
        EventCategory(name=u"ekonomia", slug="ekonomia"),
        EventCategory(name=u"wojskowość / obronność", slug="wojskowosc"),
        EventCategory(name=u"prawo", slug="prawo"),
    ])


def reverse_func(apps, schema_editor):
    EventCategory = apps.get_model("events", "EventCategory")
    db_alias = schema_editor.connection.alias
    EventCategory.objects.using(db_alias).filter(name=u"polityka krajowa", slug="polityka-krajowa").delete()
    EventCategory.objects.using(db_alias).\
        filter(name=u"polityka międzynarodowa", slug="polityka-miedzynarodowa").delete()
    EventCategory.objects.using(db_alias).filter(name=u"ekonomia", slug="ekonomia").delete()
    EventCategory.objects.using(db_alias).filter(name=u"wojskowość / obronność", slug="wojskowosc").delete()
    EventCategory.objects.using(db_alias).filter(name=u"prawo", slug="prawo").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20170601_0154'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
