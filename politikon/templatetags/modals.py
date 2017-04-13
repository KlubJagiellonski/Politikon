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


@register.inclusion_tag('modals/authenticated.html')
def authenticated_modals(user):
    return {
        'user': user,
    }


@register.inclusion_tag('modals/anonymous.html')
def anonymous_modals(user):
    return {
        'user': user,
    }


@register.inclusion_tag('modals/all.html')
def choose_modal(user, event):
    return {
        'user': user,
        'event': event,
    }

