from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, ListView, DetailView

from models import UserProfile

def login(request):
    return HttpResponsePermanentRedirect('/')


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UsersView(ListView):
    """
    Users list
    """
    def get_queryset(self):
        """
        Users list
        :return:
        :rtype: QuerySet
        """
        return UserProfile.objects.filter(is_active=True, is_deleted=False)[:30]


class UserDetailView(DetailView):
    model = UserProfile
