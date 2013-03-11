from coffin.shortcuts import render_to_response

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator

from events.models import *
from . import tasks


from fandjango.decorators import facebook_authorization_required

import hashlib
import hmac
import json

import logging
logger = logging.getLogger(__name__)


@facebook_authorization_required
def home(request):
    ctx = {
        'featured_events': list(Event.objects.get_featured_events()[:4]),
        'latest_events': list(Event.objects.get_latest_events())
    }

    ctx['people'] = Event.objects.associate_people_with_events(request.user, ctx['featured_events'] + ctx['latest_events'])

    return render_to_response('canvas/home.html', ctx, RequestContext(request))


class RealtimeUpdatesView(View):
    def _update_users(self, entries):
        for entry in entries:
            facebook_id = entry.get("uid")

            changed_fields = entry.get("changed_fields", [])
            changed_fields_count = len(changed_fields)

            if "friends" in changed_fields:
                tasks.add_facebook_user_friends_sync_task(facebook_id)
                changed_fields_count -= 1

            if changed_fields_count > 0:
                tasks.add_facebook_user_sync_task(facebook_id)

    def _check_signature(self, request):
        challenge = u'sha1=' + hmac.new(
            settings.FACEBOOK_APPLICATION_SECRET_KEY,
            msg=request.body,
            digestmod=hashlib.sha1
        ).hexdigest()

        if 'HTTP_X_HUB_SIGNATURE' in request.META and request.META['HTTP_X_HUB_SIGNATURE'] == challenge:
            return True

    def get(self, request):
        if settings.FACEBOOK_REALTIME_VERIFY_TOKEN != request.GET.get('hub.verify_token'):
            return HttpResponseForbidden("")

        return HttpResponse(request.GET.get("hub.challenge", ""))

    def post(self, request):
        if not self._check_signature(request):
            return HttpResponseForbidden("Bad signature.")

        try:
            message = json.loads(request.body)
        except Exception as e:
            logger.exception("Received malformed realtime update POST from Facebook.")
            return HttpResponseBadRequest("")

        updated_object = message.get('object')
        entries = message.get('entry', [])

        if updated_object == "user":
            self._update_users(entries)

        return HttpResponse("")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RealtimeUpdatesView, self).dispatch(*args, **kwargs)