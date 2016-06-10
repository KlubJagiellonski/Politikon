from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy

from .views import UsersListView, UserDetailView, UserUpdateView, UserProfileDetailView, PortfolioListView, \
    NotificationsListView, TransactionsListView


urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('home')},
        name='logout'),
    url(r'^rank/$', UsersListView.as_view(), name='rank'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name='user'),
    url(r'^(?P<pk>[0-9]+)/zawartoscportfela/$', PortfolioListView.as_view(), name='user_portfolio'),
    url(r'^(?P<pk>[0-9]+)/powiadomieniaowynikach/$', NotificationsListView.as_view(), name='user_notifications'),
    url(r'^(?P<pk>[0-9]+)/historiatransakcji/$', TransactionsListView.as_view(), name='user_transactions'),
    url(r'^user_settings/$', UserUpdateView.as_view(), name='user_settings'),
    url(r'^user_profile/$', UserProfileDetailView.as_view(),
        name='user_profile'),
)
