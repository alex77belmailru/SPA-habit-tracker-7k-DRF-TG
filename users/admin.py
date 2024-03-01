from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'is_staff', 'is_superuser', 'tg_user_name', 'tg_user_id')
    list_editable = ('email', 'is_active', 'is_staff', 'is_superuser', 'tg_user_name', 'tg_user_id')
    ordering = ('id',)
