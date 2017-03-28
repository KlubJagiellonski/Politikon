from rest_framework import serializers

from .models import Event, Transaction, Bet


class EventProposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'small_image', 'big_image', 'description', 'estimated_end_date')

    small_image = serializers.ImageField(required=False)
    big_image = serializers.ImageField(required=False)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = '__all__'
