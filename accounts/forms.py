# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile


class UserProfileAvatarForm(forms.ModelForm):
    """A form for updating user avatar.
    """

    class Meta:
        model = UserProfile
        fields = ['avatar']

    def clean(self):
        super(UserProfileAvatarForm, self).clean()
        print self.cleaned_data
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """A form for updating user data, part 1. Includes name, website and user
    description.
    """

    class Meta:
        model = UserProfile
        fields = ['name', 'web_site', 'description']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['web_site'].required = False
        self.fields['description'].required = False

    def clean(self):
        super(UserProfileForm, self).clean()
        print self.cleaned_data
        return self.cleaned_data


class UserProfileEmailForm(forms.ModelForm):
    """A form for updating user data, part 2. Includes passwords and emails
    fields.
    """
    email = forms.CharField(label='Twój adres e-mail',
                            widget=forms.EmailInput, required=False)
    checkemail = forms.CharField(label='wpisz ponownie adres e-mail',
                             widget=forms.EmailInput, required=False)

    class Meta:
        model = UserProfile
        fields = []

    def clean(self):
        super(UserProfileEmailForm, self).clean()
        print self.cleaned_data
        if self.cleaned_data.get('email') != \
                self.cleaned_data.get('checkemail'):
            self._errors['checkemail'] = 'Email addresses do not match.'
            # raise ValidationError('Email addresses do not match.')
        return self.cleaned_data
