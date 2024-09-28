from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authenticate.models import CustomUserModel
from userprofile.models import UserProfileModel
from users.serializers import UsersListSerializer, UserDetailSerializer


class UsersPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 30


class UsersListView(generics.ListAPIView):
    """
    Get users list details.
    """

    queryset = UserProfileModel.objects.all().order_by("-user__date_joined")
    serializer_class = UsersListSerializer
    permission_classes = [AllowAny]
    pagination_class = UsersPagination


class UserDetailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
        user = get_object_or_404(CustomUserModel, pk=user_id)  # Check if user exists
        profile, created = UserProfileModel.objects.get_or_create(
            user=user
        )  # Ensure profile exists
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class FriendsListView(generics.ListAPIView):
    """
    Get only friends users list details.
    """

    queryset = UserProfileModel.objects.all().filter(is_friend=True).order_by("id")
    serializer_class = UsersListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UsersPagination
