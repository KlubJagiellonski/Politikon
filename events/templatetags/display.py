from django import template

from events.models import Event


register = template.Library()


@register.inclusion_tag('render_bet.html')
def render_bet(event, bet, render_current):
    return {
        'event': event,
        'bet': bet,
        'render_current': render_current
    }


@register.inclusion_tag('render_event.html')
def render_event(event, bet):
    return {
        'event': event,
        'bet': bet,
    }


@register.inclusion_tag('render_events.html')
def render_events(events):
    return {
        'events': events,
    }


@register.inclusion_tag('render_featured_event.html')
def render_featured_event(event):
    return {
        'event': event,
    }


@register.inclusion_tag('render_featured_events.html')
def render_featured_events(events):
    return {
        'events': events,
    }


@register.inclusion_tag('render_bet_status.html')
def render_bet_status(bet):
    return {
        'bet': bet,
    }


@register.filter
def outcome(event):
    """Usage, {{ event|get_outcome_class }}"""
    if event.outcome == Event.EVENT_OUTCOME_CHOICES.FINISHED_YES:
        return " finished finished-yes"
    elif event.outcome == Event.EVENT_OUTCOME_CHOICES.FINISHED_NO:
        return " finished finished-no"
    elif event.outcome == Event.EVENT_OUTCOME_CHOICES.CANCELLED:
        return " finished finished-cancelled"
    else:
        return ""


@register.inclusion_tag('finish_date.html')
def render_finish_date(event):
    return {
        'event': event,
    }
