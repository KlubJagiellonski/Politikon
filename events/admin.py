# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.db import models
from django.forms import Textarea

from .exceptions import EventAlreadyFinished
from .forms import EventForm
from .models import Bet, Event, Transaction

from taggit_helpers import TaggitCounter, TaggitListFilter, TaggitTabularInline


class EventAdmin(TaggitCounter, admin.ModelAdmin):
    form = EventForm

    formfield_overrides = {
        # models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    fieldsets = (
        (u'Główne', {'fields': ('description', 'estimated_end_date', 'small_image', 'big_image', 'title',
                                'is_featured', 'is_front', 'tags')}),
        ('Social media', {'fields': ('short_title', 'title_fb_yes', 'title_fb_no', 'twitter_tag')}),
        (u'Rozwiązanie wydarzenia', {'fields': ('solve_event', 'end_date', 'outcome', 'resolved_by')}),
        ('Dane statystyczne', {'fields': ('B', 'current_buy_for_price', 'current_buy_against_price',
                                          'current_sell_for_price', 'current_sell_against_price',
                                          'last_transaction_date', 'Q_for', 'Q_against', 'turnover',
                                          'absolute_price_change', 'price_change')})
    )

    readonly_fields = [
        'resolved_by',
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

    list_display = ['id', 'title', 'is_featured', 'twitter_tag', 'taggit_counter', 'outcome',
                    'created_date', 'created_by', 'estimated_end_date', 'resolved_by', 'end_date']

    list_filter = ['outcome', TaggitListFilter, 'is_featured', 'estimated_end_date', 'created_date', 'created_by']
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
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
