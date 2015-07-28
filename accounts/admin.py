from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
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


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
	fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'name', 'last_login', 'is_admin', 'is_active')
    search_fields = ['username', 'name']
    list_filter = ('is_admin', 'is_active')
    ordering = ('id', )
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (None, {'fields': ('name',)}),
        (None, {'fields': ('total_cash', 'total_given_cash')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2'), 'classes': ('wide',)}),
        (None, {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')})
    )

admin.site.register(User, UserAdmin)
