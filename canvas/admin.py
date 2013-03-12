from django.contrib import admin
from .models import FacebookUser
from fandjango.models import User


admin.site.unregister(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'facebook_id', 'authorized', 'created_at', 'last_seen_at']


admin.site.register(FacebookUser, UserAdmin)
