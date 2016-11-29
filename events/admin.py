# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.db import models
from django.forms import Textarea, TextInput

from .exceptions import EventNotInProgress
from .forms import EventForm
from .models import Bet, Event, Transaction


class EventAdmin(admin.ModelAdmin):
    form = EventForm

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    fieldsets = (
        (u'Główne', {'fields': ('description', 'estimated_end_date', 'small_image', 'big_image', 'title',
                                'is_featured', 'tags')}),
        ('Social media', {'fields': ('short_title', 'title_fb_yes', 'title_fb_no', 'twitter_tag')}),
        (u'Rozwiązanie wydarzenia', {'fields': ('end_date', 'outcome', 'outcome_reason')}),
        ('Dane statystyczne', {'fields': ('B', 'current_buy_for_price', 'current_buy_against_price',
                                          'current_sell_for_price', 'current_sell_against_price',
                                          'last_transaction_date', 'Q_for', 'Q_against', 'turnover',
                                          'absolute_price_change', 'price_change')})
    )

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

    list_display = ['id', 'title', 'is_featured', 'twitter_tag', 'outcome',
                    'created_date', 'created_by', 'estimated_end_date', 'end_date']

    list_filter = ['outcome', 'is_featured', 'estimated_end_date', 'created_date', 'created_by']
    search_fields = ['title']
    change_form_template = 'events/admin/change_form.html'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'outcome', 'has', 'bought', 'sold', 'bought_avg_price',
                    'sold_avg_price', 'rewarded_total']
    list_filter = ['user', 'event', 'outcome']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'type', 'date', 'quantity', 'price']
    list_filter = ['user', 'event', 'type', 'date']


EventAdmin.list_per_page = 10000
admin.site.register(Event, EventAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Transaction, TransactionAdmin)
