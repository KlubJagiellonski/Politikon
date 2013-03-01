from coffin.shortcuts import render_to_response
from django.template import RequestContext

from events.models import *


def home(request):
    ctx = {
        'featured_events': Event.objects.get_featured_events()[:4],
        'latest_events': Event.objects.get_latest_events()
    }

    return render_to_response('canvas/home.html', ctx, RequestContext(request))
