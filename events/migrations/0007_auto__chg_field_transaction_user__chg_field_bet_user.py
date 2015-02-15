# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Transaction.user'
        db.alter_column(u'events_transaction', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User']))

        # Changing field 'Bet.user'
        db.alter_column(u'events_bet', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User']))

    # def backwards(self, orm):

        # Changing field 'Transaction.user'
        # db.alter_column(u'events_transaction', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fandjango.User']))

        # Changing field 'Bet.user'
        # db.alter_column(u'events_bet', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fandjango.User']))

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'total_cash': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_given_cash': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'})
        },
        u'events.bet': {
            'Meta': {'object_name': 'Bet'},
            'bought': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bought_avg_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'has': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rewarded_total': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sold_avg_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'events.event': {
            'B': ('django.db.models.fields.FloatField', [], {'default': '5'}),
            'Meta': {'object_name': 'Event'},
            'Q_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'Q_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'big_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_buy_against_price': ('django.db.models.fields.FloatField', [], {'default': '50.0'}),
            'current_buy_for_price': ('django.db.models.fields.FloatField', [], {'default': '50.0'}),
            'current_sell_against_price': ('django.db.models.fields.FloatField', [], {'default': '50.0'}),
            'current_sell_for_price': ('django.db.models.fields.FloatField', [], {'default': '50.0'}),
            'descrition': ('django.db.models.fields.TextField', [], {}),
            'estimated_end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_transaction_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'outcome': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'short_title': ('django.db.models.fields.TextField', [], {}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'events.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
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

    complete_apps = ['events']