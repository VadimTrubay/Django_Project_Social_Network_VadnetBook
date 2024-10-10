from rest_framework.response import Response
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Dialog, Message
from .serializers import DialogSerializer, MessageSerializer, DialogDetailSerializer


class DialogViewSet(viewsets.ModelViewSet):
    queryset = Dialog.objects.all().order_by('-updated_at')
    serializer_class = DialogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Pass the request context to the serializer so it has access to the request user
        serializer.save()

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return DialogDetailSerializer
        return DialogSerializer

    def get_serializer_context(self):
        # Include the request context in the serializer
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        self.perform_destroy(instance)
        return Response({"id": instance_id}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user
        # Получаем ID диалога из URL параметров
        dialog_id = self.kwargs.get('dialog_pk')

        # Проверяем, существует ли диалог и принадлежит ли он текущему пользователю
        dialog = Dialog.objects.filter(id=dialog_id, users=user).first()
        if not dialog:
            return Message.objects.none()

        # Возвращаем все сообщения для данного диалога
        return Message.objects.filter(dialog=dialog).order_by('created_at')

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя в качестве отправителя и связываем сообщение с диалогом
        dialog_id = self.kwargs.get('dialog_pk')
        dialog = Dialog.objects.filter(id=dialog_id, users=self.request.user).first()

        if dialog:
            serializer.save(sender=self.request.user, dialog=dialog)
        else:
            raise serializers.ValidationError("Invalid dialog.")
