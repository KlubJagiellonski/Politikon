# -*- coding: utf-8 -*-
from django import template

from cms.models import Page

register = template.Library()


@register.inclusion_tag('cms/pages_menu.html')
def published_pages():
    return {
        'published_pages': Page.objects.filter(is_published=True),
    }

