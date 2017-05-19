from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from .views import HomeView, acme_challenge, change_language, agree_on_cookie_store
from events.urls import api_urls as event_api

from django.contrib import admin
admin.autodiscover()


api_urls = [
    url(r'events/', include(event_api, namespace='api-events')),
    url(r'^auth/', include('djoser.urls.authtoken'))
]

urlpatterns = patterns(
    '',
    url(r'^change_language/(?P<lang>(pl|en|lt))$', change_language, name='change_language'),
    url('', include('social_django.urls', namespace='social')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^api/', include(api_urls)),
    url(r'^.well-known/acme-challenge/(?P<acme>\w+)$', acme_challenge, name='acme_challenge'),
    url(r'^agree-on-cookie-store$', agree_on_cookie_store, name='agree_on_cookie_store'),
)

urlpatterns += i18n_patterns(
    '',
    # Admin url patterns
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    # User authentication url patternsapi
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    # Application url patterns
    url(r'^', include('events.urls', namespace='events')),

    # CMS pages
    url(r'^news/', include('cms.urls', namespace='cms')),

    url(r'^$', HomeView.as_view(), name='home')
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
