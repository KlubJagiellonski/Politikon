from django.conf.urls import patterns, url

from .views import EventDetailView, EventFacebookObjectDetailView, EventsListView


urlpatterns = patterns('',
    url(r'^fbobjects/event/(?P<pk>\d+)/$', EventFacebookObjectDetailView.as_view(), name="event_facebook_object_detail"),
    url(r'^event/(?P<pk>\d+)-[a-zA-Z0-9\-]+$', EventDetailView.as_view(), name="event_detail"),
    url(r'^events/$', EventsListView.as_view(), {'mode': 'popular'}, name="events"),
    url(r'^events/(?P<mode>popular|latest|changed|finished)$', EventsListView.as_view(), name="events"),
    url(r'^event/(?P<event_id>\d+)/transaction/create/$', 'events.views.create_transaction', name="create_transaction"),
    url(r'^bets/viewed/$', 'events.views.bets_viewed', name='bets_viewed'),
)
