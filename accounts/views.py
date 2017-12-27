# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.utils.translation import ugettext as _

from .forms import (
    UserProfileAvatarForm, UserProfileForm, UserProfileEmailForm,
    UserSelfRegisterForm
)
from .models import UserProfile, Team

from events.models import Bet, Transaction
from politikon.decorators import class_view_decorator
from politikon.forms import MultiFormsView

# these bellow imports are for login function
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse


PORTFOLIO_ON_PAGE = 12
NOTIFICATIONS_ON_PAGE = 10
TRANSACTIONS_ON_PAGE = 10


@class_view_decorator(login_required)
class UserUpdateView(MultiFormsView):
    """
    User settings
    """
    # TODO: nie do końca o to chodziło, ale jest lepiej
    template_name = 'accounts/user_settings.html'
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
    template_name = 'accounts/userprofile_detail.html'

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
    template_name = 'accounts/user_detail.html'

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
    template_name = 'accounts/portfolio.html'
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
    template_name = 'accounts/notifications.html'
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
    template_name = 'accounts/transactions.html'
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
    template_name = 'accounts/rank.html'

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
            'best_monthly': UserProfile.objects.get_best_monthly(),
            'team_leaders': Team.objects.all().order_by('avg_weekly_result')
        })
        return context

class UsersGroupListView(ListView):
    """
    Users list in rank
    """
    template_name = 'accounts/groups.html'

    def get_queryset(self):
        """
        Users list
        :return:
        :rtype: QuerySet
        """
        return UserProfile.objects.get_best_overall()

    def get_context_data(self, *args, **kwargs):
        context = super(UsersGroupListView, self).get_context_data(*args, **kwargs)

        context.update({
            'group': Team.objects.all().filter(id=self.kwargs['pk'])
        })
        context.update({
            'group_users': UserProfile.objects.get_user_by_group(self.kwargs['pk'])
        })
        return context

class UserProfileCreateView(CreateView):
    """
    Create user when he chose e-mail registration from popup on website
    """
    model = UserProfile
    form_class = UserSelfRegisterForm

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super(UserProfileCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        User is created, return message to ajax.
        :return:
        """
        results = super(UserProfileCreateView, self).form_valid(form)
        # results.url - url to new user profile
        message = _('Your account is inactive yet. Please wait for the verification. Thank you.')
        return JsonResponse({'message': message})

    def render_to_response(self, context, **response_kwargs):
        """

        :param context:
        :param response_kwargs:
        :return:
        """
        response = {}
        if hasattr(context['form'], 'errors'):
            response['errors'] = {}
            for field_name, error_message in context['form'].errors.items():
                response['errors'][field_name] = error_message
        else:
            pass
        return JsonResponse(response)


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        response = {}
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())
            return JsonResponse({'redirect_to': redirect_to})
        else:
            if hasattr(form, 'errors'):
                response['errors'] = {}
                for field_name, error_message in form.errors.items():
                    response['errors'][field_name] = error_message
            else:
                pass
        return JsonResponse(response)

    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
