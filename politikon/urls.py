from django.conf import settings
from django.conf.urls import patterns, include, url

from .views import HomeView, acme_challenge

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Admin url patterns
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    # User authentication url patterns
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    # Application url patterns
    url(r'^', include('events.urls', namespace='events')),
    url(r'^.well-known/acme-challenge/sJN3Ermg6w3afMwhPJ2PPlatJ9RXlWFDTeDnHzccpdU',
        acme_challenge, name='acme_challenge'),

    url(r'^$', HomeView.as_view(), name='home')
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
    )
