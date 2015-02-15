from django.contrib import admin
from accounts.models import FacebookUser
from accounts.models import UserProfile


admin.site.unregister(UserProfile)


class UserAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'facebook_id', 'authorized', 'created_at', 'last_seen_at']


admin.site.register(FacebookUser, UserAdmin)
