from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import exceptions, serializers
from .models import CustomUserModel


class SigninSerializer(serializers.Serializer):
    """
    Serializer for user signin.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = CustomUserModel.objects.get(email=email)
        except CustomUserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid email or password")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid email or password")

        access_token = AccessToken.for_user(user)
        return {"access_token": str(access_token)}


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = CustomUserModel.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        access_token = AccessToken.for_user(user)
        return {"access_token": str(access_token)}


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = (
            "id",
            "username",
            "email",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "username",
            "email",
            "status",
            "first_name",
            "last_name",
            "website_page",
            "github_page",
            "linkedin_page",
            "looking_from_job",
            "job_skills",
            "about_me",
            "birth_date",
            "profile_picture",
            "phone_number",
            "date_joined",
        )
        model = CustomUserModel


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "username",
            "followed",
            "status",
            "profile_picture",
        )
        model = CustomUserModel
