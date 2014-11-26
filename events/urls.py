from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^fbobjects/event/(?P<event_id>\d+)/$', 'events.views.event_facebook_object_detail', name="event_facebook_object_detail"),
    url(r'^event/(?P<event_id>\d+)/$', 'events.views.event_detail', name="event_detail"),
    url(r'^event/(?P<event_id>\d+)/transaction/create/$', 'events.views.create_transaction', name="create_transaction"),

    url(r'^/$', 'events.home', name="home"),    
)
