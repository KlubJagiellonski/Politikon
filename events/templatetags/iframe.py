# -*- coding: utf-8 -*-
from django import template


register = template.Library()


@register.inclusion_tag('iframes/iframe-small.html', takes_context=True)
def small_iframe(context):
    return context
