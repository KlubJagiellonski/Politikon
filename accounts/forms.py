# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile


class UserProfileAvatarForm(forms.ModelForm):
    """A form for updating user avatar.
    """

    class Meta:
        model = UserProfile
        fields = ['avatar']


class UserProfileForm(forms.ModelForm):
    """A form for updating user data, part 1. Includes name, website and user
    description.
    """

    class Meta:
        model = UserProfile
        fields = ['name', 'web_site', 'description']


class UserProfileEmailForm(forms.ModelForm):
    """A form for updating user data, part 2. Includes passwords and emails
    fields.
    """
    # old_password = forms.CharField(label='wpisz obecne hasło',
                                   # widget=forms.PasswordInput)
    # password1 = forms.CharField(label='wpisz nowe hasło',
                                   # widget=forms.PasswordInput)
    # password2 = forms.CharField(label='wpisz ponownie nowe hasło',
                                   # widget=forms.PasswordInput)
    email1 = forms.CharField(label='Twój adres e-mail',
                            widget=forms.EmailInput)
    email2 = forms.CharField(label='wpisz ponownie adres e-mail',
                             widget=forms.EmailInput)

    # def clean_old_password(self):
        # """Check if old password matches user's password."""
        # old_password = self.cleaned_data.get('old_password')
        # if not self.user.check_password(old_password):
            # raise forms.ValidationError(_("Invalid password"))
        # return old_password

    # def clean_new_password2(self):
        # """Check that two password entries match"""
        # password1 = self.cleaned_data.get('password1')
        # password2 = self.cleaned_data.get('password2')
        # if password1 != password2:
            # raise forms.ValidationError(_("Passwords didn't match."))
        # return password2

    # def save(self, commit=True):
        # """Save the provided password in hashed format"""
        # user = super(UserProfileEmailForm, self).save(commit=False)
        # user.set_password(self.cleaned_data['password1'])
        # if commit:
            # user.save()
        # return user

    class Meta:
        model = UserProfile
        fields = []
