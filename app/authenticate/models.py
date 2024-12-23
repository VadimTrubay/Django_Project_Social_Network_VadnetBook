import uuid
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    """
    Custom user model with additional fields for user identification and additional
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # Auto create UUID
    username = models.CharField(max_length=50, unique=False, blank=False, null=False)
    email = models.EmailField(
        validators=[EmailValidator()], unique=True, blank=False, null=False
    )
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    # Отношение подписок
    following = models.ManyToManyField(
        "self", through="UserRelationship", symmetrical=False, related_name="followers"
    )
    USERNAME_FIELD = "email"  # Используем email для аутентификации
    REQUIRED_FIELDS = ["username"]  # Поле username все еще требуется

    # def __str__(self):
    #     return self.username


class UserRelationship(models.Model):
    follower = models.ForeignKey(
        CustomUserModel, related_name="following_set", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomUserModel, related_name="follower_set", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")  # Запрещаем дублирующиеся связи

    def __str__(self):
        return f"{self.follower} -> {self.following}"
