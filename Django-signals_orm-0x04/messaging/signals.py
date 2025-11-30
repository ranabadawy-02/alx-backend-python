from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create a notification when a new message is sent."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a message is saved, check if it's being edited.
    If yes, store the old content in MessageHistory.
    """
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)

        if old_message.content != instance.content:
            # Mark message as edited
            instance.edited = True

            # Save old content in history
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    """
    Clean up all messages, notifications, and history related to the deleted user.
    """

    # Delete all messages sent by the user
    Message.objects.filter(sender=instance).delete()

    # Delete all messages received by the user
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Delete all message history where the user was the editor
    MessageHistory.objects.filter(edited_by=instance).delete()
