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
            "date_joined",
        )  # Add any other fields you need


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = (
            "username",
            "first_name",
            "last_name",
        )


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
    user = EditUserSerializer()

    class Meta:
        model = UserProfileModel
        fields = (
            "user",
            "website_page",
            "github_page",
            "linkedin_page",
            "looking_from_job",
            "job_skills",
            "about_me",
            "birth_date",
            "phone_number",
        )

    def update(self, instance, validated_data):
        # Обновляем данные пользователя
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = EditUserSerializer(
                instance.user, data=user_data, partial=True
            )
            if user_serializer.is_valid():
                user_serializer.save()

        # Обновляем данные профиля
        return super().update(instance, validated_data)


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
