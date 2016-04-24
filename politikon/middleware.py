import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils.timezone import now

from accounts.models import UserProfile


logger = logging.getLogger(__name__)


class SetLastVisitMiddleware(object):
    def process_response(self, request, response):
        try:
            if request.user.is_authenticated():
                # Update last visit time after request finished processing.
                UserProfile.objects.filter(pk=request.user.pk).update(last_visit=now())
        except AttributeError as e:
            logger.exception(
                "Fatal error saving user last visit: %s" % e
            )
        return response


class BasicAuthMiddleware(object):

    def unauthed(self):
        response = HttpResponse("""<html><title>Auth required</title><body>
                                <h1>Authorization Required</h1></body>
                                </html>""", content_type="text/html")
        response['WWW-Authenticate'] = 'Basic realm="Development"'
        response.status_code = 401
        return response

    def process_request(self, request):
        if hasattr(settings, 'BASICAUTH') and settings.BASICAUTH:
            if 'HTTP_AUTHORIZATION' is not request.META:
                return self.unauthed()
            else:
                authentication = request.META['HTTP_AUTHORIZATION']
                (authmeth, auth) = authentication.split(' ', 1)
                if 'basic' != authmeth.lower():
                    return self.unauthed()
                auth = auth.strip().decode('base64')
                username, password = auth.split(':', 1)
                if username == settings.BASICAUTH_USERNAME and \
                        password == settings.BASICAUTH_PASSWORD:
                    return None

                return self.unauthed()

# from https://github.com/MidwestCommunications/django-hostname-redirects/


def _get_redirect(new_hostname, request):
    new_location = '%s://%s%s' % (
        request.is_secure() and 'https' or 'http',
        new_hostname,
        request.get_full_path()
    )
    return HttpResponsePermanentRedirect(new_location)


class HostnameRedirectMiddleware(object):
    def process_request(self, request):
        server_name = request.META['HTTP_HOST']
        catchall = getattr(settings,
                           'CATCHALL_REDIRECT_HOSTNAME', None)
        # if catchall hostname is set, verify that the current
        # hostname is valid, and redirect if not
        if catchall:
            if server_name != catchall:
                return _get_redirect(catchall, request)
        return None
