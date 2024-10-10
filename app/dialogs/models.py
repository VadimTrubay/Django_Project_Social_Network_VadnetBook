import uuid

from django.db import models

from authenticate.models import CustomUserModel


class Dialog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(CustomUserModel, related_name="dialogs")

    def __str__(self):
        return (
            f"Dialog between: {', '.join(user.username for user in self.users.all())}"
        )


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
