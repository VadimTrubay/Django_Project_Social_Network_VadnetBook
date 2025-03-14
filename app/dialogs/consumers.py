import asyncio
import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import close_old_connections

from .models import Message, Dialog
from .serializers import MessageSerializer

from channels.db import database_sync_to_async


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        close_old_connections()
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        self.user = user
        dialog_id = self.scope['url_route']['kwargs']['dialog_id']  # Получаем dialog_id из URL
        await self.accept()

        # Получаем диалог из базы данных
        dialog = await self.get_dialog(dialog_id, self.user)
        if not dialog:
            await self.close()  # Если диалог не найден или доступ запрещен
            return

        self.dialog_id = dialog_id
        self.group_name = f"dialog_{dialog_id}"

        # Подключаем пользователя к группе
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("WebSocket connection accepted")

        # Отправляем все сообщения для этого диалога при подключении
        messages = await self.get_messages(dialog_id)  # Это должна быть асинхронная операция
        print(messages)

        # Сериализуем и отправляем все сообщения
        # await self.send_all_messages(messages)

    async def send_all_messages(self, messages):
        """
        Метод для отправки всех сериализованных сообщений через WebSocket.
        """
        # Собираем задачи для отправки сообщений в список
        tasks = []
        for message in messages:
        #     # Получаем сериализованное сообщение
            serialized_message = await self.serialize_message(message)
            tasks.append(self.send_message(serialized_message))
        #
        # # Параллельно отправляем все сообщения
        await asyncio.gather(*tasks)

    async def send_message(self, serialized_message):
        """
        Метод для отправки одного сообщения через WebSocket.
        """
        await self.send(text_data=json.dumps({"message": serialized_message}, cls=UUIDEncoder))

    async def disconnect(self, close_code):
        # Отключаем пользователя от группы при разрыве соединения
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        dialog_id = data.get("dialog_id")
        message_content = data.get("content")

        if not dialog_id:
            await self.send(text_data=json.dumps({"error": "Dialog ID is required"}))
            return

        if not message_content:
            await self.send(
                text_data=json.dumps({"error": "Message content cannot be empty"})
            )
            return

        # Проверяем доступ к диалогу
        dialog = await self.get_dialog(dialog_id, self.user)
        if not dialog:
            await self.send(
                text_data=json.dumps({"error": "Dialog not found or access denied"})
            )
            return

        # Создание нового сообщения
        message = await self.create_message(dialog, message_content)

        # Сериализуем сообщение
        serialized_message = await self.serialize_message(message)

        # Рассылаем новое сообщение всем участникам диалога
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": serialized_message,
            },
        )

    async def chat_message(self, event):
        # Отправляем сообщение всем подключенным пользователям
        await self.send(text_data=json.dumps(event["message"], cls=UUIDEncoder))

    # Используем database_sync_to_async для работы с сериализатором в асинхронном контексте
    @database_sync_to_async
    def serialize_message_sync(self, message):
        # Сериализуем сообщение с использованием сериализатора
        return MessageSerializer(message).data

    async def serialize_message(self, message):
        return await self.serialize_message_sync(message)

    @database_sync_to_async
    def get_dialog(self, dialog_id, user):
        """
        Получаем диалог для данного пользователя.
        """
        return Dialog.objects.filter(id=dialog_id, users=user).first()

    @database_sync_to_async
    def get_messages(self, dialog_id):
        try:
            # Используем select_related для оптимизации запросов
            return (Message.objects.filter(dialog_id=dialog_id)
                    # .select_related("sender")
            )
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, dialog, content):
        """
        Создание нового сообщения в указанном диалоге.
        """
        return Message.objects.create(dialog=dialog, sender=self.user, content=content)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)
