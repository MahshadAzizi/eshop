from django.contrib import admin

from users.models import User


@admin.register(User)
class SimpleUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_active', 'is_staff', 'date_joined')
    readonly_fields = ('date_joined',)
