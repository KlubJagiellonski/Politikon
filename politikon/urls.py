from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from events import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#   Admin url patterns
    url(r'^admin/', include(admin.site.urls)),

#   User authentication url patterns
    url(r'^facebook/', include('fandjango.urls')),

#   Application url patterns
    url(r'^canvas/', include('canvas.urls', namespace="canvas")),
    url(r'^canvas/events/', include('events.urls', namespace="events")),

    url(r'^/$', views.home),        
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
