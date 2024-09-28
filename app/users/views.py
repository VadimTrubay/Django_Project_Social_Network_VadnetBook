from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    GenericAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authenticate.models import CustomUserModel, UserRelationship
from userprofile.models import UserProfileModel
from users.serializers import (
    UsersListSerializer,
    UserDetailSerializer,
    UserRelationshipSerializer,
    FollowersListSerializer,
    FollowingListSerializer,
)


class UsersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class UsersListView(ListAPIView):
    """
    Get users list details excluding the current user.
    """

    serializer_class = UsersListSerializer
    permission_classes = [AllowAny]
    pagination_class = UsersPagination

    def get_queryset(self):
        # Получаем текущего пользователя
        current_user = self.request.user

        # Возвращаем всех пользователей, кроме текущего
        return UserProfileModel.objects.exclude(user=current_user).order_by(
            "-user__date_joined"
        )


class UserDetailView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
        user = get_object_or_404(CustomUserModel, pk=user_id)  # Check if user exists
        profile, created = UserProfileModel.objects.get_or_create(
            user=user
        )  # Ensure profile exists
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class FollowUserView(CreateAPIView):
    """
    Create a new relationship between the current user and the user to follow.
    """

    serializer_class = UserRelationshipSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            "request": self.request
        }  # Передаем текущего пользователя в сериализатор

    def post(self, request, *args, **kwargs):
        user_to_follow_id = self.kwargs[
            "user_id"
        ]  # Получаем ID пользователя для подписки
        print(user_to_follow_id)

        # Попробуем найти пользователя с указанным UUID
        try:
            user_to_follow = CustomUserModel.objects.get(id=user_to_follow_id)
        except CustomUserModel.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Передаем UUID пользователя для валидации и создания подписки
        serializer = self.get_serializer(data={"following": user_to_follow.id})
        serializer.is_valid(raise_exception=True)

        # Сохраняем с текущим пользователем как подписчиком
        serializer.save(follower=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnfollowUserView(DestroyAPIView):
    """
    Delete the relationship between the current user and the user to unfollow.
    """

    serializer_class = UserRelationshipSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_to_unfollow = CustomUserModel.objects.get(
            id=self.kwargs["user_id"]
        )  # Используем UUID
        return UserRelationship.objects.get(
            follower=self.request.user, following=user_to_unfollow
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowersListView(ListAPIView):
    """
    Get list of users who are following the current user.
    """

    serializer_class = FollowersListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UsersPagination

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Получаем всех пользователей, которые подписаны на текущего пользователя
        followers_relationships = UserRelationship.objects.filter(following=user)

        # Возвращаем профили пользователей, которые подписаны на текущего пользователя
        return UserProfileModel.objects.filter(
            user__in=[rel.follower for rel in followers_relationships]
        )

    def get_serializer_context(self):
        """
        Добавляем request в контекст сериализатора.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})  # Передаем request в контекст
        return context


class FollowingListView(ListAPIView):
    """
    Get list of users the current user is following.
    """

    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UsersPagination

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Получаем всех пользователей, на которых подписан текущий пользователь
        following_relationships = UserRelationship.objects.filter(follower=user)

        # Возвращаем профили пользователей, на которых подписан текущий пользователь
        return UserProfileModel.objects.filter(
            user__in=[rel.following for rel in following_relationships]
        )

    def get_serializer_context(self):
        """
        Добавляем request в контекст сериализатора.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})  # Передаем request в контекст
        return context
