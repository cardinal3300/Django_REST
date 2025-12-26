from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Дополнительно", {"fields": ("phone", "city", "avatar")}),
        (
            "Права",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Системные поля",
            {
                "fields": (
                    "last_login",
                )
        }
        )
    )
    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)
    list_display = ("email", "phone", "city", "is_staff", "last_login")
    search_fields = ("email", "phone", "city")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
