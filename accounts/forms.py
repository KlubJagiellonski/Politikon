# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.admin import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile


class UserCreationForm(forms.ModelForm):
    """
    Form for creating new users. Includes all the required fields
    and repeated password. Used on admin site.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords didn't match.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserSelfRegisterForm(forms.ModelForm):
    """A form for creating new users from popup on website."""
    checkemail = forms.EmailField(label='Repeat email')
    regulamin = forms.BooleanField(label='Acknowledge')

    class Meta:
        model = UserProfile
        fields = ['password', 'username', 'email', 'checkemail', 'regulamin']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserSelfRegisterForm, self).save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAvatarForm(forms.ModelForm):
    """
    A form for updating user avatar.
    """

    class Meta:
        model = UserProfile
        fields = ['avatar']


class UserProfileForm(forms.ModelForm):
    """
    A form for updating user data, part 1. Includes name, website and user
    description.
    """

    class Meta:
        model = UserProfile
        fields = ['name', 'web_site', 'description']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['web_site'].required = False
        self.fields['description'].required = False


class UserProfileEmailForm(forms.ModelForm):
    """
    A form for updating user data, part 2. Includes passwords and emails
    fields.
    """
    email = forms.CharField(label='Twój adres e-mail', widget=forms.EmailInput, required=False)
    checkemail = forms.CharField(label='wpisz ponownie adres e-mail', widget=forms.EmailInput,
                                 required=False)

    class Meta:
        model = UserProfile
        fields = []

    def clean(self):
        super(UserProfileEmailForm, self).clean()
        if self.cleaned_data.get('email') != self.cleaned_data.get('checkemail'):
            self._errors['checkemail'] = 'Email addresses do not match.'
            # raise ValidationError('Email addresses do not match.')
        return self.cleaned_data
