from rest_framework import serializers

from authenticate.models import CustomUserModel, UserRelationship
from userprofile.models import UserProfileModel
from userprofile.serializers import UserSerializer


class UsersListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    is_friend = (
        serializers.SerializerMethodField()
    )  # Добавляем новое поле в сериализатор

    class Meta:
        model = UserProfileModel
        fields = (
            "id",
            "user",  # Полная информация о пользователе
            "status",
            "profile_picture",
            "is_friend",  # Новое поле для определения подписки
        )

    def get_is_friend(self, obj):
        request_user = self.context["request"].user

        # Проверяем, является ли пользователь аутентифицированным
        if not request_user.is_authenticated:
            return False  # Возвращаем False, если пользователь не аутентифицирован

        # Проверяем подписку только для авторизованных пользователей
        return UserRelationship.objects.filter(
            follower=request_user, following=obj.user
        ).exists()


class UserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use nested serializer to display full user details
    is_friend = (
        serializers.SerializerMethodField()
    )  # Добавляем новое поле в сериализатор

    class Meta:
        model = UserProfileModel
        fields = (
            "id",
            "user",  # Now returns full user information
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
            "is_friend",  # Новое поле для определения подписки
        )

    def get_is_friend(self, obj):
        request_user = self.context["request"].user

        # Проверяем, является ли пользователь аутентифицированным
        if not request_user.is_authenticated:
            return False  # Возвращаем False, если пользователь не аутентифицирован

        # Проверяем подписку только для авторизованных пользователей
        return UserRelationship.objects.filter(
            follower=request_user, following=obj.user
        ).exists()


class UserRelationshipSerializer(serializers.ModelSerializer):
    follower = UserSerializer(
        read_only=True
    )  # Информация о подписчике (автоматически заполняется)
    following = serializers.SlugRelatedField(
        slug_field="id", queryset=CustomUserModel.objects.all()
    )

    class Meta:
        model = UserRelationship
        fields = ["follower", "following", "created_at"]

    def create(self, validated_data):
        request_user = self.context["request"].user  # Получаем текущего пользователя
        following_user = validated_data["following"]
        # Создаем подписку
        relationship, created = UserRelationship.objects.get_or_create(
            follower=request_user, following=following_user
        )
        if not created:
            raise serializers.ValidationError("Вы уже подписаны на этого пользователя.")
        return relationship


class FollowersListSerializer(UsersListSerializer):
    pass


class FollowingListSerializer(UsersListSerializer):
    pass
