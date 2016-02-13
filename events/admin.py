# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Bet, Event, Transaction, RelatedEvent
from .forms import EventForm


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    readonly_fields = [
        'end_date',
        'outcome',
        'current_buy_for_price',
        'current_buy_against_price',
        'current_sell_for_price',
        'current_sell_against_price',
        'last_transaction_date',
        'Q_for',
        'Q_against',
    ]

    list_display = ['id', 'title', 'is_featured', 'outcome', 'created_date',
                    'estimated_end_date', 'end_date', 'current_buy_for_price',
                    'current_buy_against_price', 'Q_for', 'Q_against']

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            if request.POST['solve_event']:
                if request.POST['solve_event'] == 'TAK':
                    obj.finish_yes()
                elif request.POST['solve_event'] == 'NIE':
                    obj.finish_no()
                elif request.POST['solve_event'] == 'ANULUJ':
                    obj.cancel()
        obj.save()


class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'outcome', 'has', 'bought', 'sold',
                    'bought_avg_price', 'sold_avg_price', 'rewarded_total']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'type', 'date', 'quantity', 'price']


class RelatedEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'related']


admin.site.register(Event, EventAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RelatedEvent, RelatedEventAdmin)
