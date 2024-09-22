import uuid
from django.db import models
from django.core.validators import EmailValidator, URLValidator
from django.contrib.auth.models import AbstractUser
from django.core import validators

from users.validators import (
    validate_file_size,
    birth_date_validator,
    phone_number_validator,
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.username, filename)


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
    website_page = models.URLField(validators=[URLValidator()], blank=True, null=True)
    github_page = models.URLField(validators=[URLValidator()], blank=True, null=True)
    linkedin_page = models.URLField(validators=[URLValidator()], blank=True, null=True)
    looking_from_job = models.BooleanField(default=False, blank=True, null=True)
    job_skills = models.TextField(max_length=500, blank=True, null=True)
    about_me = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.CharField(
        max_length=10,
        validators=[birth_date_validator],
        help_text="Enter birthdate 'DD.MM.YYYY'",
        blank=True,
        null=True,
    )
    profile_picture = models.ImageField(
        upload_to="static/images/",
        default="profile_pictures/profile_picture_default.jpg",
        validators=[
            validate_file_size,
            validators.FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            ),
        ],
    )  # Profile picture field
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_number_validator],
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username
