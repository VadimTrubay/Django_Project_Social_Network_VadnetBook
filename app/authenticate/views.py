from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from authenticate.models import CustomUserModel
from authenticate.serializers import (
    SignUpSerializer,
    SignInSerializer,
    CustomUserSerializer,
)


class SignUpView(generics.CreateAPIView):
    """
    Register new user.
    """

    queryset = CustomUserModel.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.save()

        return Response(token_data)


class SignInView(TokenViewBase):
    """
    Authenticate user.
    """

    serializer_class = SignInSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    """
    Get user details.
    """

    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
