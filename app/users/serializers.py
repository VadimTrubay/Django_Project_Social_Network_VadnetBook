from rest_framework import serializers
from userprofile.models import UserProfileModel
from userprofile.serializers import UserSerializer


class UsersListSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use nested serializer to display full user details

    class Meta:
        model = UserProfileModel
        fields = (
            "id",
            "user",  # Now returns full user information
            "is_friend",
            "status",
            "profile_picture",
        )
