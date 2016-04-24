from django import template
register = template.Library()


@register.inclusion_tag('user_home.html')
def user_home(user):
    return {
        'user': user
    }


@register.inclusion_tag('user_rank.html')
def user_rank(user, profit=None, counter=1):
    return {
        'user': user,
        'profit': profit,
        'counter': counter,
    }
