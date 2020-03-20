from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from portal.models import Profile

"""
creating the profile class to display on admin
"""


class ProfileExtend(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileExtend,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_role', 'is_active', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser')
    list_select_related = ('profile',)

    def get_role(self, instance):
        return instance.profile.role

    get_role.short_description = 'Role'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()

        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
