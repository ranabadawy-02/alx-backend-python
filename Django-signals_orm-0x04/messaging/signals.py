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
