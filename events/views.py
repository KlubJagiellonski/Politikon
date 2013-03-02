from coffin.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bladepolska.http import JSONResponse, JSONResponseBadRequest
import json

from .exceptions import *
from .models import *


def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        if request.user:
            user_bets_qs = Bet.objects.get_users_bets_for_events(request.user, [event])
            user_bets = list(user_bets_qs)
        else:
            user_bets = []
    except Event.DoesNotExist:
        raise Http404

    ctx = {
        'event': event,
        'event_dict': event.event_dict,
        'bets': user_bets,
        'bets_dict': [bet.bet_dict for bet in user_bets]
    }

    return render_to_response('events/event_detail.html', ctx, RequestContext(request))


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def create_transaction(request, event_id):
    try:
        buy = bool(request.POST['buy'])
        outcome = request.POST['outcome']
        for_price = float(request.POST['for_price'])
    except:
        return HttpResponseBadRequest(_("Something went wrong, try again in a few seconds."))

    try:
        if buy:
            user, event, bet = Bet.objects.buy_a_bet(request.user, event_id, outcome, for_price)
        else:
            user, event, bet = Bet.objects.sell_a_bet(request.user, event_id, outcome, for_price)
    except NonexistantEvent:
        raise Http404
    except PriceMismatch as e:
        result = {
            'error': unicode(e),
            'updates': {
                'events': [
                    e.updated_event.event_dict
                ]
            }
        }

        return JSONResponseBadRequest(json.dumps(result))
    except InsufficientCash as e:
        result = {
            'error': unicode(e),
            'updates': {
                'user': [
                    e.updated_user.user_dict
                ]
            }
        }

        return JSONResponseBadRequest(json.dumps(result))
    except InsufficientBets as e:
        result = {
            'error': unicode(e),
            'updates': {
                'bets': [
                    e.updated_bet.bet_dict
                ]
            }
        }

        return JSONResponseBadRequest(json.dumps(result))
    except EventNotInProgress as e:
        result = {
            'error': unicode(e),
        }

        return JSONResponseBadRequest(json.dumps(result))
    except UnknownOutcome as e:
        result = {
            'error': unicode(e),
        }

        return JSONResponseBadRequest(json.dumps(result))

    result = {
        'updates': {
            'bets': [
                bet.bet_dict
            ],
            'events': [
                event.event_dict
            ],
            'user': [
                user.statistics_dict
            ]
        }
    }

    return JSONResponse(json.dumps(result))
