# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.email'
        db.add_column(u'accounts_userprofile', 'email',
                      self.gf('django.db.models.fields.CharField')(default=u'tgrf@tgrf.eu', unique=True, max_length=1024),
                      keep_default=False)

        # Adding field 'UserProfile.is_authenticated'
        db.add_column(u'accounts_userprofile', 'is_authenticated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.email'
        db.delete_column(u'accounts_userprofile', 'email')

        # Deleting field 'UserProfile.is_authenticated'
        db.delete_column(u'accounts_userprofile', 'is_authenticated')


    models = {
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'to': u"orm['accounts.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_authenticated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'portfolio_value': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'total_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'total_given_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'})
        },
        u'accounts.userprofilesnapshot': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'UserProfileSnapshot', 'db_table': "u'accounts_userprofile_snapshot'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portfolio_value': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'snapshot_of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snapshots'", 'on_delete': 'models.PROTECT', 'to': u"orm['accounts.UserProfile']"}),
            'total_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'total_given_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'})
        }
    }

    complete_apps = ['accounts']