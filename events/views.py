from coffin.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bladepolska.http import JSONResponse, JSONResponseBadRequest
import json
import logging
logger = logging.getLogger(__name__)

from .exceptions import *
from .models import *

from fandjango.decorators import facebook_authorization_required

def create_bets_dict(user, events):
    bets = dict()
    if user is not None:
        bets = Bet.objects.get_users_bets_for_events(user, events)
        bets = dict((bet.event_id, bet) for bet in bets)

    all_bets = dict()
    for event in events:
        if event.id in bets and bets[event.id].has>0:
            bet = bets[event.id]
            all_bets[event.id]={
                'has_any' : True,
                'buyYES': bet.outcome,
                'buyNO' : not bet.outcome,
                'outcomeYES' : "YES" if bet.outcome else "NO",
                'outcomeNO' : "YES" if bet.outcome else "NO",
                'priceYES' : event.current_buy_for_price if bet.outcome else event.current_sell_against_price,
                'priceNO' : event.current_sell_for_price if bet.outcome else event.current_buy_against_price,
                'textYES' : "+" if bet.outcome else "-",
                'textNO' : "-" if bet.outcome else "+",
                'has' : bet.has,
                'classOutcome' : "YES" if bet.outcome else "NO",
                'textOutcome' : "TAK" if bet.outcome else "NIE",
                'avgPrice' : round(bet.bought_avg_price,2),
            }
        else:
            all_bets[event.id]={
                'has_any' : False,
                'buyYES': True,
                'buyNO' : True,
                'outcomeYES' : "YES",
                'outcomeNO' : "NO",
                'priceYES' : event.current_buy_for_price,
                'priceNO' : event.current_buy_against_price,
                'textYES' : "TAK",
                'textNO' : "NIE"
            }

    return all_bets

def index(request):
    ctx = {
        'front_event' : Event.objects.get_front_event(),
        'featured_events': list(Event.objects.get_featured_events()),
        'latest_events': list(Event.objects.get_events('latest'))
    }

    ctx['bets'] = create_bets_dict(request.user, [ctx['front_event']]+ctx['featured_events']+ctx['latest_events'])
# TODO: what's that?
#    ctx['people'] = Event.objects.associate_people_with_events(request.user, ctx['featured_events'] + ctx['latest_events'])

    return render_to_response('index.html', ctx, RequestContext(request))

def events(request, mode):
    ctx = {
        'events': list(Event.objects.get_events(mode)),
    }
    ctx['bets'] = create_bets_dict(request.user, ctx['events'])

    return render_to_response('events/events.html', ctx, RequestContext(request))

def event_facebook_object_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404

    ctx = {
        'event': event,
    }

    return render_to_response('fb_objects/events/event_detail.html', ctx, RequestContext(request))

def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        if request.user and request.user.is_authenticated():
            user_bets_qs = Bet.objects.get_users_bets_for_events(request.user, [event])
            user_bets = list(user_bets_qs)
        else:
            user_bets = []
    except Event.DoesNotExist:
        raise Http404

    ctx = {
        'event': event,
        'bet' : create_bets_dict(request.user, [event])[event.id]
#TODO: ???
#        'event_dict': event.event_dict,
#        'bets': user_bets,
#        'bet_dicts': [bet.bet_dict for bet in user_bets]
    }

    return render_to_response('events/event_detail.html', ctx, RequestContext(request))


@login_required
@require_http_methods(["POST"])
@csrf_exempt
@transaction.commit_on_success()
def create_transaction(request, event_id):
    data = json.loads(request.body)
    try:
        buy = (data['buy'] == 'True')
        outcome = data['outcome']
        for_price = data['for_price']
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
                    e.updated_user.statistics_dict
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
            'user': user.statistics_dict
        }
    }

    return JSONResponse(json.dumps(result))
