# -*- coding: utf-8 -*-
from django.contrib import admin

from models import *


class EventAdmin(admin.ModelAdmin):
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

    # Uncomment to enable solving multiple events @ once
    # actions = [finish_yes, finish_no, cancel]


class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'outcome', 'has', 'bought', 'sold', 'bought_avg_price', 'sold_avg_price', 'rewarded_total']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'type', 'date', 'quantity', 'price']


admin.site.register(Event, EventAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Transaction, TransactionAdmin)
