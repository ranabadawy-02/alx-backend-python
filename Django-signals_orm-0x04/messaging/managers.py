# messaging/managers.py
from django.db import models
from django.db.models import Prefetch


class MessageQuerySet(models.QuerySet):
    def with_sender_receiver(self):
        return self.select_related("sender", "receiver")

    def with_replies(self):
        # Prefetch replies and also select_related the reply's sender/receiver to avoid N+1
        return self.prefetch_related(
            Prefetch("replies", queryset=self.select_related("sender", "receiver"))
        )


class MessageManager(models.Manager):
    """
    Default manager providing useful helpers for threaded retrieval.
    """
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def threaded(self):
        return self.get_queryset().with_sender_receiver().with_replies()



class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )
