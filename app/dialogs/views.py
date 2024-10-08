from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Dialog, Message
from .serializers import DialogSerializer, MessageSerializer, DialogDetailSerializer


class DialogViewSet(viewsets.ModelViewSet):
    queryset = Dialog.objects.all()
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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
