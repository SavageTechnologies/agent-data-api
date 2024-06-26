from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "email", "last_login", "date_joined", "updated_at", "created_at"]
    list_display = ["id", "username", "first_name", "last_name", "is_staff", "is_superuser","is_active", "last_login", "updated_at", "created_at"]
    list_editable = ["first_name", "last_name" ]
    search_fields = [
        "username",
    ]
    list_filter = [
        "is_superuser",
    ]



