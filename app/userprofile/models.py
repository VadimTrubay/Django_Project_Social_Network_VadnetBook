from django.db import models
from django.core.validators import URLValidator
from cloudinary.models import CloudinaryField

from authenticate.models import CustomUserModel
from utils.validators import (
    birth_date_validator,
    phone_number_validator,
)
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfileModel(models.Model):
    """
    Custom user profile model with additional fields for user identification and additional
    """

    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    is_friend = models.BooleanField(default=False, blank=True)
    status = models.CharField(max_length=50, blank=True, null=True)
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
    profile_picture = CloudinaryField(
        "image",
        transformation={"width": 500, "height": 500, "crop": "fill"},
        blank=True,
        null=True,
    )  # Profile picture cloudinary field
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_number_validator],
        blank=True,
        null=True,
    )

    @receiver(post_save, sender=CustomUserModel)
    def create_user_profile(sender, instance, created, **kwargs):
        """Создание профиля пользователя при регистрации"""
        if created:
            UserProfileModel.objects.create(user=instance)

    @receiver
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username
