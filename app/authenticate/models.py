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
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(
        validators=[EmailValidator()], unique=True, blank=False, null=False
    )

    def __str__(self):
        return self.username
