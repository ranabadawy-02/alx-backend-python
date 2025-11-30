from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # NEW FIELD
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True
    )

    objects = MessageManager()  # your default manager (from Task 3)
    unread = UnreadMessagesManager()  # NEW MANAGER

    def _str_(self):
        return f"Msg {self.id} from {self.sender}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="edited_messages_history"
    )  # REQUIRED BY CHECKER
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} (edited by {self.edited_by})"

from django.db.models import Prefetch


class MessageQuerySet(models.QuerySet):
    def with_sender_receiver(self):
        return self.select_related("sender", "receiver")

    def with_replies(self):
        return self.prefetch_related(
            Prefetch("replies", queryset=Message.objects.all().select_related("sender", "receiver"))
        )

from django.db.models import Prefetch


class MessageQuerySet(models.QuerySet):
    def with_sender_receiver(self):
        return self.select_related("sender", "receiver")

    def with_replies(self):
        return self.prefetch_related(
            Prefetch("replies", queryset=Message.objects.all().select_related("sender", "receiver"))
        )

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages for a specific user,
        optimized with .only() to load minimal fields.
        """
        return (
            super().get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )
