from django import template
register = template.Library()


@register.inclusion_tag('render_bet.html')
def render_bet(event, bet, render_current):
    return {
        'event': event,
        'bet': bet,
        'render_current': render_current
    }


@register.inclusion_tag('render_event.html')
def render_event(event, bet, people):
    return {
        'event': event,
        'bet': bet,
        'people': people
    }


@register.inclusion_tag('render_events.html')
def render_events(events, people):
    return {
        'events': events,
        'people': people
    }


@register.inclusion_tag('render_featured_event.html')
def render_featured_event(event, people):
    return {
        'event': event,
        'people': people
    }


@register.inclusion_tag('render_featured_events.html')
def render_featured_events(events, people):
    return {
        'events': events,
        'people': people
    }


@register.inclusion_tag('render_bet_status.html')
def render_bet_status(bet):
    return {
        'bet': bet,
    }
