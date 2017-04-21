from django.conf.urls import patterns, url

from .api import (
    CreateEventView,
    EventList, EventDetail,
    BetList, BetDetail,
    TransactionList, TransactionDetail
)
from .views import EventDetailView, EventFacebookObjectDetailView, EventsListView


api_urls = [
    url(r'^event/$', EventList.as_view(), name='event-list'),
    url(r'^event/create/$', CreateEventView.as_view(), name='event-create'),
    url(r'^event/(?P<pk>\d+)$', EventDetail.as_view(), name='event-detail'),
    url(r'^bet/$', BetList.as_view(), name='bet-list'),
    url(r'^bet/(?P<pk>\d+)$', BetDetail.as_view(), name='bet-detail'),
    url(r'^transaction/$', TransactionList.as_view(), name='transaction-list'),
    url(r'^transaction/(?P<pk>\d+)$', TransactionDetail.as_view(), name='transaction-detail'),
]

urlpatterns = patterns(
    '',
    url(r'^fbobjects/event/(?P<pk>\d+)/$', EventFacebookObjectDetailView.as_view(),
        name="event_facebook_object_detail"),
    url(r'^event/(?P<pk>\d+)-[a-zA-Z0-9\-]+$', EventDetailView.as_view(), name="event_detail"),
    url(r'^events/$', EventsListView.as_view(), {'mode': 'latest'}, name="events"),
    url(r'^events/(?P<mode>popular|last-minute|latest|changed|random|finished|draft)/$',
        EventsListView.as_view(),
        name="events"),
    url(r'^event/(?P<event_id>\d+)/transaction/create/$', 'events.views.create_transaction',
        name="create_transaction"),
    url(r'^event/(?P<event_id>\d+)/resolve/$', 'events.views.resolve_event',
        name="resolve_event"),
    url(r'^bets/viewed/$', 'events.views.bets_viewed', name='bets_viewed'),
)
