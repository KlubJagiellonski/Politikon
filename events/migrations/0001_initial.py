# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('short_title', self.gf('django.db.models.fields.TextField')()),
            ('descrition', self.gf('django.db.models.fields.TextField')()),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('estimated_end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('current_buy_price', self.gf('django.db.models.fields.FloatField')(default=50.0)),
            ('current_sell_price', self.gf('django.db.models.fields.FloatField')(default=50.0)),
            ('last_transaction_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('Q_for', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('Q_against', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('B', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding model 'Bet'
        db.create_table(u'events_bet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            # ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fandjango.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('outcome', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bought', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('sold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('bought_avg_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('sold_avg_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('rewarded_total', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'events', ['Bet'])

        # Adding model 'Transaction'
        db.create_table(u'events_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            # ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fandjango.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('outcome', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('direction_buy', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'events', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Deleting model 'Bet'
        db.delete_table(u'events_bet')

        # Deleting model 'Transaction'
        db.delete_table(u'events_transaction')


    models = {
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
            # 'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fandjango.User']"})
        },
        u'events.event': {
            'B': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'Event'},
            'Q_against': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'Q_for': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_buy_price': ('django.db.models.fields.FloatField', [], {'default': '50.0'}),
            'current_sell_price': ('django.db.models.fields.FloatField', [], {'default': '50.0'}),
            'descrition': ('django.db.models.fields.TextField', [], {}),
            'estimated_end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_transaction_date': ('django.db.models.fields.DateTimeField', [], {}),
            'short_title': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'events.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direction_buy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            # 'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            # 'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fandjango.User']"})
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