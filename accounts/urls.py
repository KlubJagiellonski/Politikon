from django.conf.urls import patterns, url

from .views import LogoutView


urlpatterns = patterns('',
    url(r'^login/$', 'accounts.views.login', name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # url(r'^logout/$', 'accounts.views.logout', name="accounts"),
)
