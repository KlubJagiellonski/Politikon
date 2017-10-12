# coding: utf-8
#
# Copyright (C) 2012 by Blade Polska s.c.
# Full rights belong to Tomek Kopczuk (@tkopczuk).
# www.bladepolska.com
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#
#    3. This notice may not be removed or altered from any source
#    distribution.
#

from django.db import models

import datetime

import copy


def copy_field(f):
    fp = copy.copy(f)

    fp.creation_counter = models.Field.creation_counter
    models.Field.creation_counter += 1

    if hasattr(f, "model"):
        del fp.attname
        del fp.column
        del fp.model

    return fp


class SnapshotAddon(object):
    """
    This main object contributes to the chosen model class by dynamically creating a model class for every snapshoted model:
        - Snapshot – which is a M:1 model to the snapshoted model
    It also sets reference fields on the snapshoted model class.
    """

    def __init__(self, **kwargs):
        self.init_kwargs = kwargs
        super(SnapshotAddon, self).__init__()

    def contribute_to_class(self, cls, name):
        def _contribute(sender, **kwargs):
            fields = self.init_kwargs.get('fields', [])

            # create Snapshot model
            model = create_snapshot_model(sender, fields)

            # set reference fields on newly created Snapshot, so it knows relevant SnapshotDelivery model and which model it snapshots.
            setattr(model, 'snapshots_model', cls)
            setattr(model, 'snapshotted_fields', fields)

            # registers AdminModel for this model.
            # admin.site.register(model, create_admin_model(model))

            # this sets a faux attribute on the model class, so that if you write
            # snapshots = SnapshotAddon()
            # then cls.snapshots will refer to SnapshotDescriptor
            descriptor = SnapshotDescriptor(model._default_manager)
            setattr(sender, name, descriptor)

        # connect to the "contribute" event chain, Django way
        models.signals.class_prepared.connect(_contribute, sender=cls, weak=False)


def create_snapshot_manager_with_pk(manager, pk_attribute, instance):
    """
    Create an Snapshot manager for a model instance, which already exists in the DB.
    Otherwise create_snapshot_manager_class is called instead.
    """
    class SnapshotWithPkManager(manager.__class__):
        def __init__(self, *arg, **kw):
            super(SnapshotWithPkManager, self).__init__(*arg, **kw)
            # reference to the model class being snapshoted
            self.model = manager.model
            # cached Snapshot instance
            self.instance = instance

        def get_snapshots(self):
            """ Forces query set to return only the relevant row as a safety precaution. """
            qs = super(SnapshotWithPkManager, self).get_query_set().filter(**{pk_attribute: instance})
            if self._db is not None:
                qs = qs.using(self._db)
            return qs

        def create_snapshot(self):
            new_snapshot = self.model(**{pk_attribute: instance, 'created_at': datetime.datetime.now()})

            fields = self.model.snapshotted_fields
            for field_name in fields:
                field_value = getattr(self.instance, field_name)
                setattr(new_snapshot, field_name, field_value)

            new_snapshot.save(force_insert=True)

    return SnapshotWithPkManager()


def create_snapshot_manager_class(manager):
    """
    Create an Snapshot manager for a model instance, which does not exist in the DB (a static class field for instance).
    """
    class SnapshotManager(manager.__class__):
        def __init__(self, *arg, **kw):
            super(SnapshotManager, self).__init__(*arg, **kw)
            # reference to the model class being snapshoted
            self.model = manager.model

    return SnapshotManager()


class SnapshotDescriptor(object):
    """
    Faux attribute on the model class, so that if you write 
    snapshots = SnapshotAddon()
    then cls.snapshots will refer to the proper manager for the particular context.
    """
    def __init__(self, manager):
        self.manager = manager
        self.pk_attribute = 'snapshot_of'

    def __get__(self, instance=None, owner=None):
        if instance is None:
            return create_snapshot_manager_class(self.manager)
        else:
            return create_snapshot_manager_with_pk(self.manager, self.pk_attribute, instance)

    def __set__(self, instance, value):
        raise AttributeError("Snapshot manager may not be edited in this manner.")


def create_snapshot_model(cls, fields=[]):
    """ Dynamically create a main Model, 1-1 with the model being snapshotted. """
    # Models must have unique names, so we create a name by suffixing model class name with 'Snapshot'
    name = cls.__name__ + 'Snapshot'

    class Meta:
        db_table = '%s_snapshot' % cls._meta.db_table
        app_label = cls._meta.app_label
        verbose_name = u'%s - snapshot' % cls._meta.verbose_name
        verbose_name_plural = u'%s - snapshoty' % cls._meta.verbose_name
        ordering = ['-created_at']

    # Set up a dictionary to simulate declarations within a class.
    attrs = {
        '__module__': cls.__module__,
        'Meta': Meta,
        'id': models.AutoField(primary_key=True),
        'created_at': models.DateTimeField(u"stworzony dnia", auto_now_add=True),
        'snapshot_of': models.ForeignKey(cls, verbose_name=u"dotyczy", null=False, on_delete=models.PROTECT, related_name="snapshots"),
        '__unicode__': lambda self: u'snapshot',
    }

    # Copy fields
    for field_name in fields:
        target_field = cls._meta.get_field_by_name(field_name)[0]
        attrs[field_name] = copy_field(target_field)

    return type(name, (models.Model,), attrs)
