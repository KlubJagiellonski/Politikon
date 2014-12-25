# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
#        ("fandjango", "0009_auto__chg_field_oauthtoken_token"),
        ("accounts", "0001_initial"),
    )
    def forwards(self, orm):
        # Adding model 'ActivityLog'
        db.create_table(u'canvas_activitylog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'canvas', ['ActivityLog'])

        # Adding model 'FacebookUser'
        db.create_table(u'canvas_facebookuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('facebook_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('facebook_username', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('authorized', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('oauth_token', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fandjango.OAuthToken'], unique=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_seen_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('facebook_friends', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('profile_photo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'canvas', ['FacebookUser'])


    def backwards(self, orm):
        # Deleting model 'ActivityLog'
        db.delete_table(u'canvas_activitylog')

        # Deleting model 'FacebookUser'
        db.delete_table(u'canvas_facebookuser')


    models = {
        u'canvas.activitylog': {
            'Meta': {'object_name': 'ActivityLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'canvas.facebookuser': {
            'Meta': {'object_name': 'FacebookUser'},
            'authorized': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'facebook_friends': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'facebook_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_seen_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fandjango.OAuthToken']", 'unique': 'True'}),
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

    complete_apps = ['canvas']