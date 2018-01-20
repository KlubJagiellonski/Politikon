import json
import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import DetailView

from .exceptions import (
    NonexistantEvent, DraftEvent, PriceMismatch, EventNotInProgress,
    UnknownOutcome, InsufficientBets, InsufficientCash, EventWaitingToBeResolved
)
from .models import Event, Bet, SolutionVote, EventCategory
from accounts.models import UserProfile
from bladepolska.http import JSONResponse, JSONResponseBadRequest
from haystack.generic_views import SearchView
# from haystack.query import SearchQuerySet


logger = logging.getLogger(__name__)


class EventsListView(SearchView):
    template_name = 'events/events.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super(EventsListView, self).get_queryset()
        if not self.request.user.is_authenticated() or not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)

        mode = self.kwargs.get('mode')
        if mode == 'popular':
            queryset = queryset.filter(outcome=Event.IN_PROGRESS).order_by('-turnover')
        elif mode == 'last-minute':
            queryset = queryset.filter(outcome=Event.IN_PROGRESS).order_by('estimated_end_date')
        elif mode == 'latest':
            queryset = queryset.filter(outcome=Event.IN_PROGRESS).order_by('-created_date')
        elif mode == 'changed':
            queryset = queryset.filter(outcome=Event.IN_PROGRESS).order_by('-absolute_price_change')
        elif mode == 'finished':
            queryset = queryset.exclude(outcome=Event.IN_PROGRESS).order_by('-end_date')
        elif mode == 'draft':
            queryset = queryset.exclude(is_published=True)

        category = self.kwargs.get('category')
        if category:
            event_category = get_object_or_404(EventCategory, slug=category)
            queryset = queryset.filter(categories__in=[event_category])

        # events = Event.objects.get_events(self.kwargs['mode'])
        # tag = self.request.GET.get('tag')
        # if tag:
        #     queryset = queryset.filter(tags__name__in=[tag]).distinct()
        for event in queryset:
            event.object.bet_line = event.object.get_user_bet(self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(EventsListView, self).get_context_data(*args, **kwargs)
        if 'mode' in self.kwargs:
            context['active'] = self.kwargs['mode']
        if 'category' in self.kwargs:
            context['active'] = self.kwargs['category']
        context['popular_tags'] = Event.tags.most_common()[:10]
        context['categories'] = EventCategory.objects.all()
        return context


class EventFacebookObjectDetailView(DetailView):
    template_name = 'events/facebook_event_detail.html'
    context_object_name = 'event'
    model = Event

    def get_object(self):
        return get_object_or_404(Event, id=self.kwargs['pk'])


class EventDetailView(DetailView):
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    model = Event

    def get_event(self):
        return get_object_or_404(Event, id=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        event = self.get_event()
        if not request.user.is_staff and not event.is_published:
            raise PermissionDenied
        return super(EventDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetailView, self).get_context_data(*args, **kwargs)
        event = self.get_event()
        user = self.request.user
        bet_line = event.get_user_bet(user)

        # Voted
        voted = None
        if user.is_staff:
            try:
                sv = SolutionVote.objects.get(user=user, event=event)
                voted = 'TAK' if sv.outcome == SolutionVote.YES else 'NIE'
            except SolutionVote.DoesNotExist:
                pass

        # Similar events
        # similar_events = SearchQuerySet().more_like_this(event)
        similar_events = [x for x in event.tags.similar_objects() if x.outcome == Event.IN_PROGRESS]
        for similar_event in similar_events:
            similar_event.bet_line = similar_event.get_user_bet(self.request.user)

        # Share module
        if bet_line:
            share_url = u'{}?vote={}'.format(
                event.get_absolute_url(),
                'true' if bet_line['outcome'] else 'false',
            )
        else:
            share_url = event.get_absolute_url()

        context.update({
            'bet_line': bet_line,
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


class EventEmbedDetailView(DetailView):
    template_name = 'events/event_embed_detail.html'
    context_object_name = 'event'
    model = Event

    def get_event(self):
        return get_object_or_404(Event, id=self.kwargs['pk'])

    @method_decorator(xframe_options_exempt)
    def dispatch(self, request, *args, **kwargs):
        event = self.get_event()
        if not event.is_published:
            raise PermissionDenied
        return super(EventEmbedDetailView, self).dispatch(request, *args, **kwargs)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
@transaction.atomic
def create_transaction(request, event_id):
    """
    Buy or sell bet
    :param request:
    :param event_id:
    :return:
    """
    data = json.loads(request.body)
    try:
        # simple params validation
        buy = bool(data['buy'])              # True - buy, False - sell
        outcome = bool(data['outcome'])      # True - YES,   False - NO
        for_price = int(data['for_price'])   # price

    except KeyError:
        return HttpResponseBadRequest(_("Something went wrong, try again in a few seconds."))
    try:
        if buy:
            user, event, bet = Bet.objects.buy_a_bet(request.user, event_id, outcome, for_price)
        else:
            user, event, bet = Bet.objects.sell_a_bet(request.user, event_id, outcome, for_price)
    except NonexistantEvent:
        raise Http404
    except (DraftEvent, EventWaitingToBeResolved) as e:
        result = {
            'error': str(e),
        }
        return JSONResponseBadRequest(json.dumps(result))
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
