from rest_framework import serializers

from .models import Event, Transaction, Bet


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id',

                  'title', 'short_title', 'twitter_tag', 'title_fb_yes',
                  'title_fb_no', 'description', 'small_image', 'big_image',
                  'is_featured', 'outcome', 'outcome_reason', 'created_date',
                  'created_by', 'estimated_end_date', 'end_date',
                  'current_buy_for_price', 'current_buy_against_price',
                  'current_sell_against_price', 'last_transaction_date',
                  'Q_for', 'Q_against', 'turnover', 'absolute_price_change',
                  'price_change', 'B')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
