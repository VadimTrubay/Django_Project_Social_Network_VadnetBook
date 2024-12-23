# Generated by Django 5.0 on 2024-09-24 11:30

import cloudinary.models
import django.core.validators
import django.db.models.deletion
import utils.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfileModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_friend", models.BooleanField(blank=True, default=False)),
                ("status", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "website_page",
                    models.URLField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                    ),
                ),
                (
                    "github_page",
                    models.URLField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                    ),
                ),
                (
                    "linkedin_page",
                    models.URLField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                    ),
                ),
                (
                    "looking_from_job",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("job_skills", models.TextField(blank=True, max_length=500, null=True)),
                ("about_me", models.TextField(blank=True, max_length=500, null=True)),
                (
                    "birth_date",
                    models.CharField(
                        blank=True,
                        help_text="Enter birthdate 'DD.MM.YYYY'",
                        max_length=10,
                        null=True,
                        validators=[utils.validators.birth_date_validator],
                    ),
                ),
                (
                    "profile_picture",
                    cloudinary.models.CloudinaryField(
                        default="profile_pictures/profile_picture_default.jpg",
                        max_length=255,
                        verbose_name="image",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        unique=True,
                        validators=[utils.validators.phone_number_validator],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
