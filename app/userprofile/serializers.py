from rest_framework import serializers

from authenticate.models import CustomUserModel
from .models import UserProfileModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )  # Add any other fields you need


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfileModel
        fields = (
            "user",
            "status",
            "website_page",
            "github_page",
            "linkedin_page",
            "looking_from_job",
            "job_skills",
            "about_me",
            "birth_date",
            "phone_number",
            "profile_picture",
        )


class EditUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileModel
        fields = (
            "website_page",
            "github_page",
            "linkedin_page",
            "looking_from_job",
            "job_skills",
            "about_me",
            "birth_date",
            "phone_number",
        )


class UserProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = ("profile_picture",)

    def update(self, instance, validated_data):
        profile_picture = validated_data.get("profile_picture", None)
        if profile_picture:
            instance.profile_picture = profile_picture  # Сохранение изображения
        instance.save()
        return instance


class UserProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = ("status",)

    def update(self, instance, validated_data):
        status = validated_data.get("status", None)
        if status:
            instance.status = status  # Сохранение status
        instance.save()
        return instance
