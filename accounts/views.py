# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .forms import UserProfileAvatarForm, UserProfileForm, UserProfileEmailForm
from .models import UserProfile

from events.models import Bet, Transaction
from politikon.decorators import class_view_decorator
from politikon.forms import MultiFormsView


PORTFOLIO_ON_PAGE = 12
NOTIFICATIONS_ON_PAGE = 10
TRANSACTIONS_ON_PAGE = 10


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
        return get_object_or_404(UserProfile, pk=self.request.session['_auth_user_id'])

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


@class_view_decorator(login_required)
class UserProfileDetailView(DetailView):
    """
    Logged user profile detail (user.id from session)
    """
    model = UserProfile
    template_name = 'userprofile_detail.html'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileDetailView, self).\
            get_context_data(*args, **kwargs)
        user = self.get_object()
        portfolio_page = Paginator(user.bets.get_in_progress(), PORTFOLIO_ON_PAGE).page(1)
        notifications_page = Paginator(Bet.objects.get_finished(user), NOTIFICATIONS_ON_PAGE).page(1)
        transactions_page = Paginator(Transaction.objects.get_user_transactions_after_reset(user),
                                           TRANSACTIONS_ON_PAGE).page(1)
        context.update(UserProfile.objects.get_user_positions(user))
        context.update({
            'user_pk': user.pk,
            'json_data': json.dumps(user.get_reputation_history()),
            'portfolio_list': portfolio_page.object_list,
            'portfolio_page': portfolio_page,
            'notifications_list': notifications_page.object_list,
            'notifications_page': notifications_page,
            'transactions_list': transactions_page.object_list,
            'transactions_page': transactions_page,
        })
        return context


class UserDetailView(DetailView):
    """
    User profile detail. Any user can see this page (user.id from url)
    """
    model = UserProfile
    template_name = 'user_detail.html'

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
        portfolio_page = Paginator(user.bets.get_in_progress(), PORTFOLIO_ON_PAGE).page(1)
        notifications_page = Paginator(Bet.objects.get_finished(user), NOTIFICATIONS_ON_PAGE).page(1)
        transactions_page = Paginator(Transaction.objects.get_user_transactions_after_reset(user),
                                           TRANSACTIONS_ON_PAGE).page(1)
        context.update(UserProfile.objects.get_user_positions(user))
        context.update({
            'user_pk': user.pk,
            'json_data': json.dumps(user.get_reputation_history()),
            'portfolio_list': portfolio_page.object_list,
            'portfolio_page': portfolio_page,
            'notifications_list': notifications_page.object_list,
            'notifications_page': notifications_page,
            'transactions_list': transactions_page.object_list,
            'transactions_page': transactions_page,
        })
        return context


class PortfolioListView(ListView):
    """
    Portfolio list in userprofile
    """
    template_name = 'portfolio.html'
    paginate_by = PORTFOLIO_ON_PAGE
    context_object_name = 'portfolio_list'

    def get_object(self):
        return UserProfile.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        user = self.get_object()
        return user.bets.get_in_progress()

    def get_context_data(self, *args, **kwargs):
        context = super(PortfolioListView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update({
            'portfolio_page': context['page_obj'],
            'object': user,
            'user_pk': user.pk,
            'json_data': json.dumps(user.get_reputation_history()),
        })
        return context


class NotificationsListView(ListView):
    """
    Notifications list in userprofile
    """
    template_name = 'notifications.html'
    paginate_by = NOTIFICATIONS_ON_PAGE
    context_object_name = 'notifications_list'

    def get_object(self):
        return UserProfile.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        user = self.get_object()
        return Bet.objects.get_finished(user)

    def get_context_data(self, *args, **kwargs):
        context = super(NotificationsListView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update({
            'notifications_page': context['page_obj'],
            'object': user,
            'user_pk': user.pk,
            'json_data': json.dumps(user.get_reputation_history()),
        })
        return context


class TransactionsListView(ListView):
    """
    Transactions list in userprofile
    """
    template_name = 'transactions.html'
    paginate_by = TRANSACTIONS_ON_PAGE
    context_object_name = 'transactions_list'

    def get_object(self):
        return UserProfile.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        user = self.get_object()
        return Transaction.objects.get_user_transactions_after_reset(user)

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionsListView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update({
            'transactions_page': context['page_obj'],
            'object': user,
            'user_pk': user.pk,
            'json_data': json.dumps(user.get_reputation_history()),
        })
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
        return UserProfile.objects.get_best_overall()

    def get_context_data(self, *args, **kwargs):
        context = super(UsersListView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated():
            context.update(UserProfile.objects.get_user_positions(user))
            context['json_data'] = json.dumps(user.get_reputation_history())
        context.update({
            'best_weekly': UserProfile.objects.get_best_weekly(),
            'best_monthly': UserProfile.objects.get_best_monthly()
        })
        return context
