# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import Team, UserProfile

from constance import config


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_elo')
    fields = ('name', 'avatar', 'get_elo')
    readonly_fields = ('get_elo',)

    def get_elo(self, instance):
        return instance.get_elo()
    get_elo.short_description = 'Elo'


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username', 'name', 'last_login', 'is_admin', 'is_active', 'is_vip', 'is_staff',
        'is_deleted', 'team', 'facebook_user', 'twitter_user', 'last_visit', 'last_transaction', 'reset_date'
    )
    search_fields = ['username', 'name']
    list_filter = ('is_admin', 'is_active', 'is_staff', 'is_deleted')
    ordering = ('id', )
    filter_horizontal = ()

    actions = ['topup', 'set_active', 'make_vip', 'block']

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'team')}),
        (None, {'fields': ('name', )}),
        (None, {'fields': ('total_cash', 'total_given_cash')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_staff', 'is_vip')}),
        (_('Important dates'), {'fields': ('last_login', )}), )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'email'),
            'classes': ('wide', )
        }),
        (None, {
            'fields': ('name', )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_admin', 'is_staff', 'is_vip')
        })
    )

    class Topup:
        def __call__(self, modeladmin, request, queryset):
            for user in queryset:
                user.topup_cash(config.ADMIN_TOPUP)

        @property
        def short_description(self):
            return u'Doładuj wybrane konta o %s' % config.ADMIN_TOPUP

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
    make_vip.short_description = u'Uczyń użytkownikiem VIP'

    def block(modeladmin, request, queryset):
        for user in queryset:
            user.is_deleted = True
            user.save(update_fields=['is_deleted'])
    block.short_description = 'Zablokuj wybrane konta'


admin.site.register(Team, TeamAdmin)
admin.site.register(UserProfile, MyUserAdmin)
