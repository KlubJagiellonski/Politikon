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
def user_rank(context, user, item_class="", profit=None, counter=1):
    return {
        'request': context['request'],
        'item_class': item_class,
        'user': user,
        'profit': profit,
        'counter': counter,
    }


@register.inclusion_tag('user_portfolio.html', takes_context=True)
def user_portfolio(context):
    return {
        'objects_list': context['portfolio_list'],
        'page_obj': context['portfolio_page'],
        'user_pk': context['user_pk'],
    }


@register.inclusion_tag('user_notifications.html', takes_context=True)
def user_notifications(context):
    return {
        'objects_list': context['notifications_list'],
        'page_obj': context['notifications_page'],
        'user_pk': context['user_pk'],
    }


@register.inclusion_tag('user_transactions.html', takes_context=True)
def user_transactions(context):
    return {
        'objects_list': context['transactions_list'],
        'page_obj': context['transactions_page'],
        'user_pk': context['user_pk'],
    }
