# -*- encoding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from constance import config

from .models import UserProfile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

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


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'name', 'last_login', 'is_admin', 'is_active',
                    'is_vip', 'is_staff', 'is_deleted', 'facebook_user',
                    'twitter_user')
    search_fields = ['username', 'name']
    list_filter = ('is_admin', 'is_active', 'is_staff', 'is_deleted')
    ordering = ('id', )
    filter_horizontal = ()

    actions = ['topup', 'set_active', 'make_vip', 'block']

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        (None, {'fields': ('name', )}),
        (None, {'fields': ('total_cash', 'total_given_cash')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_staff',
                                       'is_vip')}),
        (_('Important dates'), {'fields': ('last_login', )}), )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'email'),
            'classes': ('wide', )
        }), (None, {'fields': ('name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_staff',
                                       'is_vip')}))

    class Topup:
        def __call__(self, request, queryset):
            for user in queryset:
                user.topup_cash(config.ADMIN_TOPUP)

        @property
        def short_description(self):
            return 'Doładuj wybrane konta o %s' % config.ADMIN_TOPUP

    topup = Topup()

    def set_active(modeladmin, request, queryset):
        for user in queryset:
            user.is_active = True
            user.save(update_fields=['is_active'])
    set_active.short_description = 'Aktywuj wybrane konta'

    def make_vip(modeladmin, request, queryset):
        for user in queryset:
            user.is_vip = True
            user.save(update_fields=['is_vip'])
    make_vip.short_description = 'Uczyń użytkownikiem VIP'

    def block(modeladmin, request, queryset):
        for user in queryset:
            user.is_deleted = True
            user.save(update_fields=['is_deleted'])
    block.short_description = 'Zablokuj wybrane konta'

admin.site.register(UserProfile, MyUserAdmin)
