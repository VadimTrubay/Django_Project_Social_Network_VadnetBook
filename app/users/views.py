from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from userprofile.models import UserProfileModel
from users.serializers import UsersListSerializer


class UsersPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 30


class UsersListView(generics.ListAPIView):
    """
    Get users list details.
    """

    queryset = UserProfileModel.objects.all().order_by("id")
    serializer_class = UsersListSerializer
    permission_classes = [AllowAny]
    pagination_class = UsersPagination


class FriendsListView(generics.ListAPIView):
    """
    Get only friends users list details.
    """

    queryset = UserProfileModel.objects.all().filter(is_friend=True).order_by("id")
    serializer_class = UsersListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UsersPagination
