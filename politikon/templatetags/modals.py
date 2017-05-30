# -*- coding: utf-8 -*-
from django import template
from django.utils import timezone

from events.models import Event, Bet

register = template.Library()


@register.inclusion_tag('modals/staff.html')
def staff_modals(event):
    return {
        'event': event,
    }


@register.inclusion_tag('modals/authenticated.html', takes_context=True)
def authenticated_modals(context, user):
    return {
        'user': user,
        'request': context.get('request')
    }


@register.inclusion_tag('modals/anonymous.html')
def anonymous_modals(user):
    return {
        'user': user,
    }


@register.inclusion_tag('modals/any.html', takes_context=True)
def anyuser_modals(context):
    return context


@register.inclusion_tag('modals/all.html', takes_context=True)
def choose_modal(context, user, event):
    return {
        'user': user,
        'event': event,
        'request': context.get('request')
    }

