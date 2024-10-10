from rest_framework import serializers
from authenticate.models import CustomUserModel
from .models import Dialog, Message


class DialogUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.CharField(
        source="userprofilemodel.profile_picture.url", read_only=True
    )

    class Meta:
        model = CustomUserModel
        fields = ["id", "username", "profile_picture"]


class DialogSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=CustomUserModel.objects.all(), write_only=True
    )

    class Meta:
        model = Dialog
        fields = ["id", "created_at", "updated_at", "users"]

    def create(self, validated_data):
        request_user = self.context["request"].user
        other_user_id = validated_data["users"]  # Получаем ID другого пользователя

        existing_dialog = (
            Dialog.objects.filter(users=request_user)
            .filter(users=other_user_id)
            .first()
        )

        if existing_dialog:
            return existing_dialog  # Возвращаем существующий диалог, если найден

        dialog = Dialog.objects.create()
        dialog.users.add(
            request_user, other_user_id
        )  # Добавляем текущего и другого пользователя
        return dialog


class DialogDetailSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Dialog
        fields = ["id", "created_at", "updated_at", "other_user"]

    def get_other_user(self, obj):
        request_user = self.context["request"].user
        # Фильтруем пользователя, чтобы вернуть только другого участника
        other_user = obj.users.exclude(id=request_user.id).first()
        return DialogUserSerializer(other_user).data if other_user else None


class MessageSerializer(serializers.ModelSerializer):
    sender = DialogUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "created_at", "updated_at", "dialog", "sender", "content"]
