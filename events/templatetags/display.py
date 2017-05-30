# -*- coding: utf-8 -*-
from django import template
from django.utils import timezone

from events.models import Bet


register = template.Library()


@register.inclusion_tag('events/render_bet.html', takes_context=True)
def render_bet(context, event):
    return {
        'event': event,
        'bet': event.get_user_bet(context['request'].user)
    }


@register.inclusion_tag('events/render_events.html', takes_context=True)
def render_events(context, events):
    try:
        r_events = [event.object for event in events]
    except AttributeError:
        r_events = events
    return {
        'events': r_events,
        'request': context.get('request')
    }


@register.inclusion_tag('events/render_featured_event.html')
def render_featured_event(event):
    return {
        'event': event,
    }


@register.inclusion_tag('events/render_featured_events.html')
def render_featured_events(events):
    return {
        'events': events,
    }


@register.inclusion_tag('events/render_bet_status.html')
def render_bet_status(bet):
    return {
        'bet': bet,
    }


@register.filter
def outcome(event):
    """Usage, {{ event|get_outcome_class }}"""
    if event.outcome == event.FINISHED_YES:
        return " finished finished-yes"
    elif event.outcome == event.FINISHED_NO:
        return " finished finished-no"
    elif event.outcome == event.CANCELLED:
        return " finished finished-cancelled"
    else:
        return ""


@register.inclusion_tag('events/finish_date.html')
def render_finish_date(event):
    state = 'finished'
    if not event.finish_date:
        return {
            'state': 'none'
        }
    if event.is_in_progress:
        state = 'no-result' if timezone.now() > event.finish_date else 'ongoing'
    return {
        'date': event.finish_date,
        'state': state
    }


@register.inclusion_tag('events/og_title.html')
def og_title(event, vote=None, user=None):
    title = event.title
    if user:
        bet = event.get_user_bet_object(user)
        if bet and bet.has > 0:
            if event.is_in_progress:
                verb = u'uważa że'
            elif bet.outcome and event.outcome == event.FINISHED_YES:
                verb = u'ma rację że'
            elif not bet.outcome and event.outcome == event.FINISHED_NO:
                verb = u'ma rację że'
            else:
                verb = u'nie ma racji że'

            if bet.outcome == bet.YES:
                title = u'%s %s %s' % (user.name, verb, event.title_fb_yes)
            else:
                title = u'%s %s %s' % (user.name, verb, event.title_fb_no)
        else:
            title = event.title

    elif vote is not None:
        if event.is_in_progress:
            verb = u'Moim zdaniem'
        elif vote == Bet.YES and event.outcome == event.FINISHED_YES:
            verb = u'Mam rację że'
        elif vote == Bet.NO and event.outcome == event.FINISHED_NO:
            verb = u'Mam rację że'
        else:
            verb = u'Nie mam racji że'

        if vote == Bet.YES:
            title = u'%s %s' % (verb, event.title_fb_yes)
        elif vote == Bet.NO:
            title = u'%s %s' % (verb, event.title_fb_no)

    return {
        'title': title
    }
