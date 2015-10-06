# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Bet, Event, Transaction
from .forms import EventForm


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    readonly_fields = [
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
                    'estimated_end_date', 'current_buy_for_price',
                    'current_buy_against_price', 'Q_for', 'Q_against']


    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            if request.POST['solve_event']:
                if request.POST['solve_event'] == 'TAK':
                    obj.outcome = obj.EVENT_OUTCOME_CHOICES.FINISHED_YES
                elif request.POST['solve_event'] == 'NIE':
                    obj.outcome = obj.EVENT_OUTCOME_CHOICES.FINISHED_NO
                elif request.POST['solve_event'] == 'ANULUJ':
                    obj.outcome = obj.EVENT_OUTCOME_CHOICES.CANCELLED
        obj.save()

    def finish_yes(self, request, queryset):
        for event in queryset:
            event.finish_yes()
    finish_yes.short_description = 'Rozstrzygnij na TAK'

    def finish_no(self, request, queryset):
        for event in queryset:
            event.finish_no()
    finish_no.short_description = 'Rozstrzygnij na NIE'

    def cancel(self, request, queryset):
        for event in queryset:
            event.cancel()
    cancel.short_description = 'Anuluj wydarzenie'


class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'outcome', 'has', 'bought', 'sold', 'bought_avg_price', 'sold_avg_price', 'rewarded_total']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'type', 'date', 'quantity', 'price']


admin.site.register(Event, EventAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Transaction, TransactionAdmin)
