from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'accounts.views.login', name="accounts"),
    url(r'^logout', 'accounts.views.logout', name="accounts"),
)
