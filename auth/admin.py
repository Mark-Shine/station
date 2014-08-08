from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import WzUser


class AccountInline(admin.StackedInline):
    model = WzUser
    can_delete = False
    verbose_name_plural = 'account'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (AccountInline, )



admin.site.register(WzUser)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)