# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
#        ("fandjango", "0009_auto__chg_field_oauthtoken_token"),
    )

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'accounts_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            # ('facebook_user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='django_user', unique=True, null=True, to=orm['fandjango.User'])),
            ('total_cash', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('total_given_cash', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'accounts', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'accounts_user')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            # 'facebook_user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'django_user'", 'unique': 'True', 'null': 'True', 'to': u"orm['fandjango.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'total_cash': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_given_cash': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'})
        }
        # u'fandjango.oauthtoken': {
        #     'Meta': {'object_name': 'OAuthToken'},
        #     'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
        #     u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        #     'issued_at': ('django.db.models.fields.DateTimeField', [], {}),
        #     'token': ('django.db.models.fields.TextField', [], {})
        # },
        # u'fandjango.user': {
        #     'Meta': {'object_name': 'User'},
        #     'authorized': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
        #     'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
        #     'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
        #     'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
        #     'facebook_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
        #     'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
        #     u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        #     'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
        #     'last_seen_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
        #     'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
        #     'oauth_token': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['fandjango.OAuthToken']", 'unique': 'True'})
        # }
    }

    complete_apps = ['accounts']