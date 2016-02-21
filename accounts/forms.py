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
    email1 = forms.CharField(label='Twój adres e-mail',
                            widget=forms.EmailInput)
    email2 = forms.CharField(label='wpisz ponownie adres e-mail',
                             widget=forms.EmailInput)

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
