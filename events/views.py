import json
import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import DetailView, ListView

from .exceptions import NonexistantEvent, PriceMismatch, EventNotInProgress, \
    UnknownOutcome, InsufficientBets, InsufficientCash
from .models import Event, Bet, Transaction, SolutionVote
from .utils import create_bets_dict
from accounts.models import UserProfile
from bladepolska.http import JSONResponse, JSONResponseBadRequest


logger = logging.getLogger(__name__)


class EventsListView(ListView):
    template_name = 'events.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        events = Event.objects.get_events(self.kwargs['mode'])
        for event in events:
            event.my_bet = event.get_user_bet(self.request.user)
        return events

    def get_context_data(self, *args, **kwargs):
        context = super(EventsListView, self).get_context_data(*args, **kwargs)
        context['active'] = self.kwargs['mode']
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

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetailView, self).get_context_data(*args, **kwargs)
        event = self.get_event()
        user = self.request.user
        bet = event.get_user_bet(user)

        # Voted
        voted = None
        if user.is_staff:
            try:
                sv = SolutionVote.objects.get(user=user, event=event)
                voted = 'TAK' if sv.outcome == sv.VOTE_OUTCOME_CHOICES.YES else 'NIE'
            except SolutionVote.DoesNotExist:
                pass

        # Similar events
        similar_events = [x for x in event.tags.similar_objects() if \
                          x.outcome == Event.EVENT_OUTCOME_CHOICES.IN_PROGRESS]
        for similar_event in similar_events:
            similar_event.my_bet = similar_event.get_user_bet(self.request.user)

        # Share module
        if bet:
            share_url = u'%s?vote=%s' % (event.get_absolute_url(), 'YES' if bet.outcome else 'NO')
        else:
            share_url = event.get_absolute_url()

        context.update({
            'bet': event.get_user_bet(user),
            'active': 1,
            'voted': voted,
            'event_dict': event.event_dict,
            'bet_social': event.get_bet_social(),
            'og_user': UserProfile.objects.filter(username=self.request.GET.get('user')).first(),
            'og_vote': self.request.GET.get('vote'),
            'similar_events': similar_events[:3],
            'share_url': share_url
        })
        return context


@login_required
@require_http_methods(["POST"])
@csrf_exempt
@transaction.atomic
def create_transaction(request, event_id):
    data = json.loads(request.body)
    try:
        buy = (data['buy'] == 'True')   # kupno, sprzedaz
        outcome = data['outcome']     # tak nie
        for_price = data['for_price']  # cena
    except:
        return HttpResponseBadRequest(_("Something went wrong, try again in a \
                                        few seconds."))
    try:
        if buy:
            user, event, bet = Bet.objects.buy_a_bet(request.user, event_id,
                                                     outcome, for_price)
        else:
            user, event, bet = Bet.objects.sell_a_bet(request.user, event_id,
                                                      outcome, for_price)
    except NonexistantEvent:
        raise Http404
    except PriceMismatch as e:
        result = {
            'error': unicode(e.message.decode('utf-8')),
            'updates': {
                'events': [
                    e.updated_event.event_dict
                ]
            }
        }
        return JSONResponseBadRequest(json.dumps(result))
    except InsufficientCash as e:
        result = {
            'error': unicode(e.message.decode('utf-8')),
            'updates': {
                'user': [
                    e.updated_user.statistics_dict
                ]
            }
        }

        return JSONResponseBadRequest(json.dumps(result))
    except InsufficientBets as e:
        result = {
            'error': unicode(e.message.decode('utf-8')),
            'updates': {
                'bets': [
                    e.updated_bet.bet_dict
                ]
            }
        }

        return JSONResponseBadRequest(json.dumps(result))
    except EventNotInProgress as e:
        result = {
            'error': unicode(e.message.decode('utf-8')),
        }

        return JSONResponseBadRequest(json.dumps(result))
    except UnknownOutcome as e:
        result = {
            'error': unicode(e.message.decode('utf-8')),
        }

        return JSONResponseBadRequest(json.dumps(result))

    request.user.last_transaction = now()
    request.user.save()
    
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


@login_required
@vary_on_headers('HTTP_X_REQUESTED_WITH')
def bets_viewed(request):
    """
    Uncheck new finished event as read
    :param request:
    :type request: WSGIRequest
    :return: json list with bet ids
    :rtype: JSONResponse
    """

    bets_id_list = request.GET.getlist('bets[]')
    bets_resolved = []
    for bet_id in bets_id_list:
        try:
            bet = Bet.objects.get(user=request.user, id=int(bet_id))
        except ValueError:
            continue
            # TODO: log somewhere or do something
        bet.is_new_resolved = False
        bet.save()
        bets_resolved.append(bet_id)

    return JSONResponse(json.dumps(bets_resolved))


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
@csrf_exempt
@transaction.atomic
def resolve_event(request, event_id):
    """
    Vote for yes or no
    :param request:
    :type request: WSGIRequest
    :param event_id: event id
    :type event_id: int
    :return:
    """
    data = json.loads(request.body)
    try:
        vote_result = Event.objects.vote_for_solution(request.user, event_id, data['outcome'])
    except EventNotInProgress as e:
        result = {
            'error': unicode(e.message.decode('utf-8')),
        }

        return JSONResponseBadRequest(json.dumps(result))

    result = {
        'updates': vote_result
    }

    return JSONResponse(json.dumps(result))
