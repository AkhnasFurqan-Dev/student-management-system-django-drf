from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    """Admin config. for custom user model."""

    list_display = ("username", "email", "role", "is_staff", "is_active")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role & Student Info", {
            "fields": ("role", "enrollment_year", "batch", "roll_number")
            }
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Profile Info", {
            "fields": ("email", "first_name", "last_name", "role", "enrollment_year", "batch", "roll_number")
            }
        ),
    )


admin.site.register(User, UserAdmin)
