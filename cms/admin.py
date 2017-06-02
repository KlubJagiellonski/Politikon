from django.contrib import admin

from .models import Page, ExtraContent, GalleryImage

from imagekit.admin import AdminThumbnail


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


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'admin_thumbnail']
    fields = ('name', 'image')
    admin_thumbnail = AdminThumbnail(image_field='image')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


admin.site.register(Page, PageAdmin)
admin.site.register(ExtraContent, ExtraContentAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
