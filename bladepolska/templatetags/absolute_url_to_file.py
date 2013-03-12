from coffin import template
register = template.Library()

from jinja2 import Markup

from bladepolska.site import current_domain


@register.filter
def absolute_url_to_file(file):
    url = file.url
    if url.startswith('/'):
        url = "http://%(domain)s%(url)s" % {
            'domain': current_domain(),
            'url': url
        }

    return Markup(url)
