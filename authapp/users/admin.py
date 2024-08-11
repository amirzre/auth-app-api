from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from authapp.users.models import BaseUser, UserProfile
from authapp.users.services import create_profile, create_user


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ("phone", "is_admin", "is_superuser", "is_active", "created_at", "updated_at")

    search_fields = ("phone",)

    list_filter = ("is_active", "is_admin", "is_superuser")

    fieldsets = (
        (None, {"fields": ("phone",)}),
        ("Booleans", {"fields": ("is_active", "is_admin", "is_superuser")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            create_user(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "email", "created_at", "updated_at")

    search_fields = ("email",)

    list_filter = ("created_at",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            create_profile(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
