from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


def login(request):
    return HttpResponsePermanentRedirect('/')


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
