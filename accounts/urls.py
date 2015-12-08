from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

from .views import UsersView, UserDetailView, user_settings_view, user_profile_view


urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('home')}, name='logout'),
    url(r'^users/$', UsersView.as_view(), name='users'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name='user'),
    url(r'^user_settings/$', user_settings_view, name='user_settings'),
    url(r'^user_profile/$', user_profile_view, name='user_profile'),
)
