from django.contrib import admin

from .models import Page, ExtraContent


class PageAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'user_profile',
        'slug',
    ]
    change_form_template = 'cms/admin/change_form.html'


class ExtraContentAdmin(admin.ModelAdmin):
    list_display = [
        'tag_code',
        'user_profile',
        'created_at',
        'updated_at',
        'lang',
    ]

admin.site.register(Page, PageAdmin)
admin.site.register(ExtraContent, ExtraContentAdmin)
