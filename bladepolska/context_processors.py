from django.conf import settings as app_settings


def settings(request):
    return {'settings': app_settings}
