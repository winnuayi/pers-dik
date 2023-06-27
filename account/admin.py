from django.contrib import admin

from account.models import CustomUser as User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'is_staff', 'is_active',)


admin.site.register(User, UserAdmin)
