from django.http import HttpResponsePermanentRedirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView

from politikon.decorators import class_view_decorator
from politikon.forms import MultipleFormsView
from .forms import UserProfileAvatarForm, UserProfileForm, UserProfileEmailForm
from .models import UserProfile


@class_view_decorator(login_required)
class UserUpdateView(MultipleFormsView):
    """
    User settings
    """
    template_name = 'accounts/user_settings.html'
    form_classes = {
        'main': UserProfileForm,
        'email': UserProfileEmailForm,
        'avatar': UserProfileAvatarForm
    }
    success_url = reverse_lazy('success')

    def main_form_valid(self, form):
        print("jaj")
        return form.main(self.request, redirect_url=self.get_success_url())

    def main_form_invalid(self, form):
        print(form.errors)
        return form.main(self.request, redirect_url=self.get_success_url())
    # def form_valid(self, form):
        # print("jaj")
        # form.save()
        # messages.success(self.request, _('Successfully updated profile.'))
        # return redirect(self.success_url)

    # def form_invalid(self, form):
        # print(form.errors)
        # for field, errors in form.errors.iteritems():
            # name = form.fields[field].label
            # form.errors[field] = [u'{name}: {error}'.format(name=name, error=e)
                                  # for e in errors]
        # return super(UserUpdateView, self).form_invalid(form)


def user_settings_view(renuest):

    user = UserProfile.objects.get(pk=request.session['_auth_user_id'])
    # messages musi zawierac tuples: tresc i czy to jest komunikat o bladzie,
    # np: ("niepoprawne stare haslo", True)
    messages = []
    if request.method == 'POST':
        if request.POST.get('user_name'):
            user.name = request.POST['user_name']
            user.description = request.POST['description']
            user.web_site = request.POST['web_site']
            user.save()
            messages.append((_("user's data updated"), False))
        else:
            if request.POST.get('checkemail'):
                if request.POST.get('email') == request.POST.get('checkemail'):
                    user.email = request.POST.get('email')
                    user.save()
                    messages.append((_("e-mail updated"), False))
                else:
                    messages.append((_("e-mails doesn't match"), False))
            if request.POST.get('oldpass') and request.POST.get('newpass'):
                if user.check_password(request.POST.get('oldpass')):
                    if request.POST.get('newpass') == request.POST.\
                            get('checkpass'):
                        user.set_password(request.POST.get('newpass'))
                        user.save()
                        messages.append((_("password updated"), False))
                    else:
                        messages.append((_("passwords doesn't match"), True))
                else:
                    messages.append((_('wrong old password'), True))
    context = {
        'user': user,
        'messages': messages,
    }
    return render(request, 'accounts/user_settings.html', context)


class UserProfileDetailView(DetailView):
    """
    User profile
    """
    model = UserProfile

    def get_object(self, **kwargs):
        return self.request.user


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
        return UserProfile.objects.filter(is_active=True,
                                          is_deleted=False)[:30]


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
