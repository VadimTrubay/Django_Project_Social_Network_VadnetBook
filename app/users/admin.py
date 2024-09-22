from django.contrib import admin
from .models import CustomUserModel

FIELDS = (
    "username",
    "email",
    "status",
    "first_name",
    "last_name",
    "phone_number",
    "looking_from_job",
    "date_joined",
    "birth_date",
    "is_staff",
    "is_active",
)


@admin.register(CustomUserModel)
class UserAdmin(admin.ModelAdmin):
    """
    Админ-панель модели CustomUserModel
    """

    list_display = FIELDS
    list_display_links = FIELDS
    # list_filter = FIELDS
    # list_editable = FIELDS
