from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, ListView, DetailView

from models import UserProfile


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
