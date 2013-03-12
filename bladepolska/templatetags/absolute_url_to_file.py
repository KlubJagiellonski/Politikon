from coffin import template
register = template.Library()

from jinja2 import Markup

from django.contrib.sites.models import Site
DOMAIN = Site.objects.get_current().domain


@register.filter
def absolute_url_to_file(file):
    url = file.url
    if url.startswith('/'):
        url = "http://%(domain)s%(url)s" % {
            'domain': DOMAIN,
            'url': url
        }

    return Markup(url)
