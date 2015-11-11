from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import RedirectView, ListView, DetailView

from models import UserProfile


def user_settings_view(request):

    user = UserProfile.objects.get(pk=request.session['_auth_user_id'])      # TODO: continue this work
    context = {
        'user': user,
    }
    return render(request, 'accounts/user_settings.html', context)


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

    def get_object(self, **kwargs):
        """
        User detail
        :return:
        :rtype: QuerySet
        """
        user_detail = super(UserDetailView, self).get_object(**kwargs)
#        user_detail.bets.all()
        return user_detail
