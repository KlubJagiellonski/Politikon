# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'accounts_user')

        # Removing M2M table for field friends on 'User'
        db.delete_table('accounts_user_friends')

        # Deleting model 'UserSnapshot'
        db.delete_table(u'accounts_user_snapshot')

        # Adding model 'UserProfile'
        db.create_table(u'accounts_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('total_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('total_given_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('portfolio_value', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
        ))
        db.send_create_signal(u'accounts', ['UserProfile'])

        # Adding M2M table for field friends on 'UserProfile'
        db.create_table(u'accounts_userprofile_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False))
        ))
        db.create_unique(u'accounts_userprofile_friends', ['from_userprofile_id', 'to_userprofile_id'])

        # Adding model 'UserProfileSnapshot'
        db.create_table(u'accounts_userprofile_snapshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('snapshot_of', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snapshots', on_delete=models.PROTECT, to=orm['accounts.UserProfile'])),
            ('total_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('total_given_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('portfolio_value', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
        ))
        db.send_create_signal(u'accounts', ['UserProfileSnapshot'])


    def backwards(self, orm):
        # Adding model 'User'
        db.create_table(u'accounts_user', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=1024, unique=True)),
            ('portfolio_value', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('facebook_user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='django_user', unique=True, null=True, on_delete=models.SET_NULL, to=orm['canvas.FacebookUser'])),
            ('total_given_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('total_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['User'])

        # Adding M2M table for field friends on 'User'
        db.create_table(u'accounts_user_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm[u'accounts.user'], null=False)),
            ('to_user', models.ForeignKey(orm[u'accounts.user'], null=False))
        ))
        db.create_unique(u'accounts_user_friends', ['from_user_id', 'to_user_id'])

        # Adding model 'UserSnapshot'
        db.create_table(u'accounts_user_snapshot', (
            ('snapshot_of', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snapshots', on_delete=models.PROTECT, to=orm['accounts.User'])),
            ('portfolio_value', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('total_given_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('total_cash', self.gf('django.db.models.fields.IntegerField')(default=0.0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'accounts', ['UserSnapshot'])

        # Deleting model 'UserProfile'
        db.delete_table(u'accounts_userprofile')

        # Removing M2M table for field friends on 'UserProfile'
        db.delete_table('accounts_userprofile_friends')

        # Deleting model 'UserProfileSnapshot'
        db.delete_table(u'accounts_userprofile_snapshot')


    models = {
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'to': u"orm['accounts.UserProfile']"}),
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