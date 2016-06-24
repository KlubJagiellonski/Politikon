from django import template
from django.conf import settings


register = template.Library()


@register.filter
def canvas_relative_url(url):
    canvas_url = settings.FACEBOOK_APPLICATION_CANVAS_URL
    if url.startswith(canvas_url):
        url = url[len(canvas_url):]

    return url
