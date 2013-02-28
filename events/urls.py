from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^event/(?P<event_id>\d+)/$', 'events.views.event_detail', name="event_detail"),
)
