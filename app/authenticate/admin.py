from django.contrib import admin

from authenticate.models import CustomUserModel

FIELDS = ("username", "email")


@admin.register(CustomUserModel)
class UserAdmin(admin.ModelAdmin):
    """
    Админ-панель модели CustomUserModel
    """

    list_display = FIELDS
    list_display_links = FIELDS
    ordering = ("username",)
    # list_filter = FIELDS
