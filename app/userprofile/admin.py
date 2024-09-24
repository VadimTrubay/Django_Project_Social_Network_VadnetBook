from django.contrib import admin
from userprofile.models import UserProfileModel


@admin.register(UserProfileModel)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель модели UserProfileModel
    """

    # pass
    # # Создаем методы для получения значений из связанных полей CustomUserModel
    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def date_joined(self, obj):
        return obj.user.date_joined

    def is_staff(self, obj):
        return obj.user.is_staff

    def is_active(self, obj):
        return obj.user.is_active

    # Поля для отображения в админке
    list_display = (
        "username",
        "status",
        "first_name",  # Поля из CustomUserModel
        "last_name",  # Поля из CustomUserModel
        "phone_number",
        "looking_from_job",
        "date_joined",  # Поля из CustomUserModel
        "birth_date",
        "is_staff",  # Поля из CustomUserModel
        "is_active",  # Поля из CustomUserModel
    )
    list_display_links = list_display
    # Убираем 'is_staff' из ordering, так как это поле не принадлежит UserProfileModel
    ordering = ("user__username",)  # Сортировка по полю user.is_staff

    # Используем пользовательские методы для фильтрации
    # list_filter = (
    # "looking_from_job", "user__is_staff", "user__is_active")  # Фильтруем по полям связанных пользователей
