from django.conf.urls import url

from .views import IndexView, PageDetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index_news'),
    url(r'^page/(?P<pk>\d+)-[a-zA-Z0-9\-]+$', PageDetailView.as_view(), name='page'),
]
