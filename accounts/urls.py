from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

from .views import UsersView, UserDetailView


urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('home')}, name='logout'),
    url(r'^users/$', UsersView.as_view(), name='users'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name='user'),
)
