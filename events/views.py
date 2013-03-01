from coffin.shortcuts import render_to_response
from django.http import Http404

from .models import *


def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except:
        raise Http404

    ctx = {
        'event': event
    }

    return render_to_response('events/event_detail.html', ctx)
