# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponseRedirect

from models import *


class SolvingEventsChangeFormMixin(object):
    def response_action(self, request, queryset):
        """
        Prefer http referer for redirect
        """
        response = super(SolvingEventsChangeFormMixin, self).response_action(request,
                queryset)
        if isinstance(response, HttpResponseRedirect):
            response['Location'] = request.META.get('HTTP_REFERER', response.url)
        return response

    def save_model(self, request, obj, form, change):
        print form
        super(SolvingEventsChangeFormMixin, self).save_model(request, obj, form, change)

    def change_view(self, request, object_id, extra_context=None):
        actions = self.get_actions(request)
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
        else:
            action_form = None
        extra_context=extra_context or {}
        extra_context['action_form'] = action_form
        return super(SolvingEventsChangeFormMixin, self).change_view(request, object_id, extra_context=extra_context)


class EventAdmin(SolvingEventsChangeFormMixin, admin.ModelAdmin):
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
    actions = [finish_yes, finish_no, cancel]


class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'outcome', 'has', 'bought', 'sold', 'bought_avg_price', 'sold_avg_price', 'rewarded_total']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'type', 'date', 'quantity', 'price']


admin.site.register(Event, EventAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Transaction, TransactionAdmin)
