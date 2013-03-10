from coffin.shortcuts import render_to_response

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from django.views.generic.base import View

from events.models import *

from fandjango.decorators import facebook_authorization_required

import hashlib
import hmac


@facebook_authorization_required
def home(request):
    ctx = {
        'featured_events': Event.objects.get_featured_events()[:4],
        'latest_events': Event.objects.get_latest_events()
    }

    return render_to_response('canvas/home.html', ctx, RequestContext(request))


class RealtimeUpdates(View):
    def check_signature(self, request):
        body = request.body
        challenge = u'sha1=' + hmac.new(
            settings.FACEBOOK_APPLICATION_SECRET_KEY,
            msg=body,
            digestmod=hashlib.sha1
        ).hexdigest()

        if request.META[u'X_HUB_SIGNATURE'] == challenge:
            return True

    def get(self, request):
        if settings.FACEBOOK_REALTIME_VERIFY_TOKEN != request.GET.get('hub.verify_token'):
            return HttpResponseForbidden("")

        return HttpResponse(request.GET.get("hub.challenge", ""))

    def post(self, request):
        if not self.check_signature(request):
            return HttpResponseForbidden("Bad signature.")

        pass
