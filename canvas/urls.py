from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'canvas.views.home', name="home"),
)
