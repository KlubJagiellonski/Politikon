# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Bet, Event, Transaction, RelatedEvent
from .forms import EventForm


class RelatedEventInline(admin.TabularInline):
    model = RelatedEvent
    fk_name = 'event'
    extra = 1


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

    list_display = ['id', 'title', 'is_featured', 'outcome', 'created_date',
                    'estimated_end_date', 'end_date', 'current_buy_for_price',
                    'current_buy_against_price', 'Q_for', 'Q_against',
                    'turnover', 'absolute_price_change', 'price_change']

    inlines = [RelatedEventInline, ]

    def save_model(self, request, obj, form, change):
        """
        Save event model from admin form
        :param request:
        :type request: HTTPRequest
        :param obj:
        :type obj: Event
        :param form:
        :type form: EventForm
        :param change:
        :type change:
        """
        if request.method == 'POST':
            if request.POST['solve_event']:
                if request.POST['solve_event'] == 'TAK':
                    obj.finish_yes()
                elif request.POST['solve_event'] == 'NIE':
                    obj.finish_no()
                elif request.POST['solve_event'] == 'ANULUJ':
                    obj.cancel()
            small_img_url = request.POST.get('download_small_image')
            if small_img_url:
                obj.download_image(small_img_url, 'small')
            big_img_url = request.POST.get('download_big_image')
            if big_img_url:
                obj.download_image(big_img_url, 'big')
        obj.save()


class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'outcome', 'has', 'bought', 'sold',
                    'bought_avg_price', 'sold_avg_price', 'rewarded_total']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'type', 'date', 'quantity', 'price']


admin.site.register(Event, EventAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Transaction, TransactionAdmin)
