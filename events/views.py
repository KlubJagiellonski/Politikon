from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from bladepolska.http import JSONResponse, JSONResponseBadRequest
import json
import logging
logger = logging.getLogger(__name__)

from .exceptions import NonexistantEvent, PriceMismatch, EventNotInProgress, \
    UnknownOutcome, InsufficientBets, InsufficientCash
from .models import Event, Bet, Transaction

from django.contrib.auth.decorators import login_required


def create_bets_dict(user, events):
    bets = dict()
    if user is not None:
        bets = Bet.objects.get_users_bets_for_events(user, events)
        bets = dict((bet.event_id, bet) for bet in bets)

    all_bets = dict()
    if len(events) > 1:
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


class EventsListView(ListView):
    template_name = 'events.html'

    def get_queryset(self):
        return Event.objects.get_events('popular')

    def get_context_data(self, *args, **kwargs):
        context = super(EventsListView, self).get_context_data(*args, **kwargs)
        events = list(Event.objects.get_events('popular'))
        context.update({
            'events': events,
            'bets': create_bets_dict(self.request.user, events)
        })
        return context


class EventFacebookObjectDetailView(DetailView):
    template_name = 'facebook_event_detail.html'
    context_object_name = 'event'
    model = Event

    def get_object(self):
        return get_object_or_404(Event, id=self.kwargs['pk'])


class EventDetailView(DetailView):
    template_name = 'event_detail.html'
    context_object_name = 'event'
    model = Event

    def get_event(self):
        return get_object_or_404(Event, id=self.kwargs['pk'])

    # def dispatch(self, request, *args, **kwargs):
        # if request.user and request.user.is_authenticated():
            # user_bets_qs = Bet.objects.get_users_bets_for_events(request.user, [event])
            # user_bets = list(user_bets_qs)
        # else:
            # user_bets = []
        # return super(EventDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetailView, self).get_context_data(*args, **kwargs)
        event = self.get_event()
        bets = create_bets_dict(self.request.user, [event])
        if event.id in bets:
            bet = bets[event.id]
        else:
            bet = None
        context.update({
            'event': event,
            'bet': bet,
            'active': 1
        })
        return context


    # ctx = {
        # 'event': event,
        # 'bet' : create_bets_dict(request.user, [event])[event.id],
        # 'active': 1,
#TODO: ???
#        'event_dict': event.event_dict,
#        'bets': user_bets,
#        'bet_dicts': [bet.bet_dict for bet in user_bets]
    # }


@login_required
@require_http_methods(["POST"])
@csrf_exempt
@transaction.atomic
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
