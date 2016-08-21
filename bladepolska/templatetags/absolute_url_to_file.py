from django import template


register = template.Library()


@register.filter
def absolute_url_to_file(file):
    return file.url
