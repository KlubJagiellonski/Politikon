# -*- coding: utf-8 -*-
from django.contrib import admin, messages

from .exceptions import EventAlreadyFinished
from .forms import EventForm
from .models import Bet, Event, Transaction, RelatedEvent


class RelatedEventInline(admin.TabularInline):
    model = RelatedEvent
    fk_name = 'event'
    extra = 1
    raw_id_fields = ('related',)
    autocomplete_lookup_fields = {
        'fk': ['related'],
    }


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
        'turnover',
        'absolute_price_change',
        'price_change',
    ]

    list_display = ['id', 'title', 'is_featured', 'outcome', 'created_date', 'estimated_end_date',
                    'resolved_by', 'end_date', 'current_buy_for_price',
                    'current_buy_against_price', 'Q_for', 'Q_against', 'turnover',
                    'absolute_price_change', 'price_change']

    inlines = [RelatedEventInline, ]

    def save_model(self, request, obj, form, change):
        # TODO: to jest najgorsze
        if request.method == 'POST':
            if request.POST['solve_event']:
                try:
                    if request.POST['solve_event'] == 'TAK':
                        obj.finish_yes()
                    elif request.POST['solve_event'] == 'NIE':
                        obj.finish_no()
                    elif request.POST['solve_event'] == 'ANULUJ':
                        obj.cancel()
                    obj.resolved_by = request.user
                except EventAlreadyFinished as e:
                    messages.error(request, e.message)
        obj.save()


class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'outcome', 'has', 'bought', 'sold', 'bought_avg_price',
                    'sold_avg_price', 'rewarded_total']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'type', 'date', 'quantity', 'price']


admin.site.register(Event, EventAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Transaction, TransactionAdmin)
