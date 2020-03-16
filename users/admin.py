from django.contrib import admin
from django.contrib.auth.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
