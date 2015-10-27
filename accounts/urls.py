from django.conf.urls import patterns, url

from .views import LogoutView, UsersView, UserDetailView


urlpatterns = patterns('',
    url(r'^login/$', 'accounts.views.login', name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^users/$', UsersView.as_view(), name='users'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name='user'),
    # url(r'^logout/$', 'accounts.views.logout', name="accounts"),
)
