from django.conf.urls import url

from .views import IndexView, PageDetailView

urlpatterns = [
    # url(r'^$', IndexView.as_view(), name='index_news'),
    url(r'^(?P<slug>\w+)$', PageDetailView.as_view(), name='page'),
]
