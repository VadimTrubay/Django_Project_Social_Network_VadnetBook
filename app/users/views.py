from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from users.models import CustomUserModel
from users.serializers import (
    SignupSerializer,
    SigninSerializer,
    CustomUserModelSerializer,
)


class SignupView(generics.CreateAPIView):
    """
    Register new user.
    """

    queryset = CustomUserModel.objects.all()
    serializer_class = SignupSerializer

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

    serializer_class = CustomUserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    Logout user.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({"message": "Successfully logout"}, status=200)
