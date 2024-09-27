from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from userprofile.models import UserProfileModel
from userprofile.serializers import (
    UserProfileSerializer,
    UserProfilePhotoSerializer,
    UserProfileStatusSerializer,
    EditUserProfileSerializer,
)


class EmptySerializer(serializers.Serializer):
    pass


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfileModel.objects.select_related("user").get(
            user=self.request.user
        )


class ProfileUpdateView(generics.UpdateAPIView):
    """
    Update the profile of the logged-in user (using PATCH only).
    """

    queryset = UserProfileModel.objects.all()
    serializer_class = EditUserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def get_object(self):
        # Return the logged-in user's profile
        return UserProfileModel.objects.get(user=self.request.user)

    # Only allow partial updates (PATCH)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProfileUpdatePhotoView(generics.UpdateAPIView):
    """
    Update the profile photo of the logged-in user (using PUT method).
    """

    serializer_class = UserProfilePhotoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def get_object(self):
        # Return the logged-in user's profile
        return UserProfileModel.objects.get(user=self.request.user)

    # Only allow full updates (PUT)
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProfileUpdateStatusView(generics.UpdateAPIView):
    """
    Update the profile status of the logged-in user (using PUT method).
    """

    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileStatusSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def get_object(self):
        return UserProfileModel.objects.get(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProfileDeleteView(generics.DestroyAPIView):
    """
    Delete the logged-in user's profile.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def get_object(self):
        # Return the logged-in user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user_id = user.id  # Store the user's ID to confirm deletion later
        user.delete()
        return Response(
            {"id": {user_id}}, status=200
        )
