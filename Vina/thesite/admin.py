from django.contrib import admin
from thesite.models import Userprofile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.


# class UserAdmin(admin.ModelAdmin):
#     fields = ['username', 'password', 'email', 'file', 'labelfile']
#     list_display = ('username', 'password', 'email', 'file', 'labelfile')
#     search_fields = ['username']


class UserprofileInline(admin.StackedInline):
    model = Userprofile
    can_delete = True
    verbose_name_plural = 'userprofile'


class UserAdmin(UserAdmin):
    inlines = (UserprofileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(UserProfile, UserAdmin)