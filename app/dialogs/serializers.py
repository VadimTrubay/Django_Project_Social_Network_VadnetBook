from django.contrib.auth import get_user_model
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
    users = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )  # Список UUID пользователей

    users_info = DialogUserSerializer(many=True, read_only=True, source="users")

    class Meta:
        model = Dialog
        fields = ["id", "created_at", "updated_at", "users", "users_info"]

    def create(self, validated_data):
        request_user = self.context["request"].user
        user_model = get_user_model()

        # Получаем список ID пользователей
        user_ids = validated_data.get("users", [])

        if not user_ids:
            raise serializers.ValidationError(
                {"users": "Необходимо указать пользователей."}
            )

        # Проверяем, существует ли другой пользователь
        try:
            other_user = user_model.objects.get(id=user_ids[0])
        except user_model.DoesNotExist:
            raise serializers.ValidationError({"users": "Пользователь не найден."})

        # Проверяем, существует ли уже диалог
        existing_dialog = (
            Dialog.objects.filter(users=request_user).filter(users=other_user).first()
        )

        if existing_dialog:
            return existing_dialog  # Если диалог уже есть, возвращаем его

        # Создаем новый диалог
        dialog = Dialog.objects.create()
        dialog.users.add(request_user, other_user)  # Добавляем пользователей
        return dialog


# class DialogSerializer(serializers.ModelSerializer):
#     users = DialogUserSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Dialog
#         fields = ["id", "created_at", "updated_at", "users"]
#
#     def create(self, validated_data):
#         request_user = self.context["request"].user
#         other_user_id = validated_data["users"]  # Получаем ID другого пользователя
#         print(other_user_id, type(other_user_id))
#
#         existing_dialog = (
#             Dialog.objects.filter(users=request_user)
#             .filter(users=other_user_id)
#             .first()
#         )
#
#         if existing_dialog:
#             return existing_dialog  # Возвращаем существующий диалог, если найден
#
#         dialog = Dialog.objects.create()
#         dialog.users.add(
#             request_user, other_user_id
#         )  # Добавляем текущего и другого пользователя
#         return dialog


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


# Оптимизация запросов в сериализаторе
class MessageSerializer(serializers.ModelSerializer):
    sender = DialogUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "created_at", "updated_at", "dialog", "sender", "content"]
        # Предзагрузка связанных объектов для уменьшения количества запросов к базе данных
        depth = 1
