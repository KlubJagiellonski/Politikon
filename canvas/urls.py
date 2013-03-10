from django.conf.urls import patterns, url

from .views import RealtimeUpdates

urlpatterns = patterns('',
    url(r'^$', 'canvas.views.home', name="home"),
    url(r'^api/v1/realtime/$', RealtimeUpdates.as_view(), name="realtime_update"),
)
