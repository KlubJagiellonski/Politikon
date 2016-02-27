# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView

from politikon.decorators import class_view_decorator
from politikon.forms import MultiFormsView
from .forms import UserProfileAvatarForm, UserProfileForm, UserProfileEmailForm
from .models import UserProfile


@class_view_decorator(login_required)
class UserUpdateView(MultiFormsView):
    """
    User settings
    """
    # TODO: nie do końca o to chodziło, ale jest lepiej
    template_name = 'user_settings.html'
    form_classes = {
        'main': UserProfileForm,
        'email': UserProfileEmailForm,
        'avatar': UserProfileAvatarForm
    }
    model = UserProfile
    success_url = reverse_lazy('accounts:user_settings')

    def get_object(self):
        return get_object_or_404(UserProfile,
                                 pk=self.request.session['_auth_user_id'])

    def main_form_valid(self, form):
        user = self.get_object()
        user.name = self.request.POST.get('name')
        user.web_site = self.request.POST.get('web_site')
        user.description = self.request.POST.get('description')
        if self.request.FILES.get('avatar'):
            user.avatar = self.request.FILES.get('avatar')
        user.save()
        return redirect(self.success_url)

    def email_form_valid(self, form):
        user = self.get_object()
        user.email = self.request.POST.get('email')
        if self.request.FILES.get('avatar'):
            user.avatar = self.request.FILES.get('avatar')
        user.save()
        return redirect(self.success_url)


class UserProfileDetailView(DetailView):
    """
    User profile
    """
    model = UserProfile
    template_name = 'userprofile_detail.html'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileDetailView, self).\
            get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update(UserProfile.objects.get_user_positions(user))
        return context


class UserDetailView(DetailView):
    model = UserProfile
    template_name = 'userprofile_detail.html'

    def get_object(self, **kwargs):
        """
        User detail
        :return:
        :rtype: QuerySet
        """
        user_detail = super(UserDetailView, self).get_object(**kwargs)
        return user_detail

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update(UserProfile.objects.get_user_positions(user))
        return context


class UsersListView(ListView):
    """
    Users list in rank
    """
    template_name = 'rank.html'

    def get_queryset(self):
        """
        Users list
        :return:
        :rtype: QuerySet
        """
        return UserProfile.objects.filter(is_active=True,
                                          is_deleted=False)[:30]
