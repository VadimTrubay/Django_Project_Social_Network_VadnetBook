from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from users.models import CustomUserModel
from users.serializers import (
    SignupSerializer,
    SigninSerializer,
    CustomUserSerializer,
    UserProfileSerializer,
    UsersListSerializer,
)


class UsersPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 100


class SignupView(generics.CreateAPIView):
    """
    Register new user.
    """

    queryset = CustomUserModel.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.save()

        return Response(token_data)


class SigninView(TokenViewBase):
    """
    Authenticate user.
    """

    serializer_class = SigninSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    """
    Get user details.
    """

    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveAPIView):
    """
    Get user profile details.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UsersDetailView(generics.ListAPIView):
    """
    Get users list details.
    """

    queryset = CustomUserModel.objects.all()
    serializer_class = UsersListSerializer
    permission_classes = [AllowAny]
    pagination_class = UsersPagination


class LogoutView(APIView):
    """
    Logout user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Successfully logout"}, status=200)
