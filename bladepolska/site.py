from django.contrib.sites.models import Site


def current_domain():
    return Site.objects.get_current().domain
