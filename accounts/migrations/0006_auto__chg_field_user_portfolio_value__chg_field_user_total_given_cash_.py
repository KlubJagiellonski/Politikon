# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'User.portfolio_value'
        db.alter_column(u'accounts_user', 'portfolio_value', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'User.total_given_cash'
        db.alter_column(u'accounts_user', 'total_given_cash', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'User.total_cash'
        db.alter_column(u'accounts_user', 'total_cash', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UserSnapshot.portfolio_value'
        db.alter_column(u'accounts_user_snapshot', 'portfolio_value', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UserSnapshot.total_given_cash'
        db.alter_column(u'accounts_user_snapshot', 'total_given_cash', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UserSnapshot.total_cash'
        db.alter_column(u'accounts_user_snapshot', 'total_cash', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'User.portfolio_value'
        db.alter_column(u'accounts_user', 'portfolio_value', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'User.total_given_cash'
        db.alter_column(u'accounts_user', 'total_given_cash', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'User.total_cash'
        db.alter_column(u'accounts_user', 'total_cash', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'UserSnapshot.portfolio_value'
        db.alter_column(u'accounts_user_snapshot', 'portfolio_value', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'UserSnapshot.total_given_cash'
        db.alter_column(u'accounts_user_snapshot', 'total_given_cash', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'UserSnapshot.total_cash'
        db.alter_column(u'accounts_user_snapshot', 'total_cash', self.gf('django.db.models.fields.FloatField')())

    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'facebook_user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'django_user'", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['canvas.FacebookUser']"}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'to': u"orm['accounts.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'portfolio_value': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'total_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'total_given_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'})
        },
        u'accounts.usersnapshot': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'UserSnapshot', 'db_table': "u'accounts_user_snapshot'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portfolio_value': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'snapshot_of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snapshots'", 'on_delete': 'models.PROTECT', 'to': u"orm['accounts.User']"}),
            'total_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'}),
            'total_given_cash': ('django.db.models.fields.IntegerField', [], {'default': '0.0'})
        },
        u'canvas.facebookuser': {
            'Meta': {'object_name': 'FacebookUser'},
            'authorized': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'facebook_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_seen_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fandjango.OAuthToken']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'profile_photo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'fandjango.oauthtoken': {
            'Meta': {'object_name': 'OAuthToken'},
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_at': ('django.db.models.fields.DateTimeField', [], {}),
            'token': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['accounts']