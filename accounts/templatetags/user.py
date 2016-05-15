from django import template
register = template.Library()


@register.inclusion_tag('user_home.html')
def user_home(user, reputation_change, is_formatted=False):
    return {
        'user': user,
        'reputation_change': reputation_change,
        'is_formatted': is_formatted
    }


@register.inclusion_tag('user_rank.html', takes_context=True)
def user_rank(context, user, profit=None, counter=1):
    return {
        'request': context['request'],
        'user': user,
        'profit': profit,
        'counter': counter,
    }
