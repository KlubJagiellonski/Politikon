from coffin.shortcuts import render_to_response

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from django.views.generic.base import View

from events.models import *

from fandjango.decorators import facebook_authorization_required


@facebook_authorization_required
def home(request):
    ctx = {
        'featured_events': Event.objects.get_featured_events()[:4],
        'latest_events': Event.objects.get_latest_events()
    }

    return render_to_response('canvas/home.html', ctx, RequestContext(request))


class RealtimeUpdates(View):
    def get(self, request):
        if settings.FACEBOOK_REALTIME_VERIFY_TOKEN != request.GET.get('hub.verify_token'):
            return HttpResponseForbidden("")

        return HttpResponse(request.GET.get("hub.challenge", ""))

    def post(self, request):
        pass
