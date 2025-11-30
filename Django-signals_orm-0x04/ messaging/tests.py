from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessagingSignalTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="pass123")
        self.receiver = User.objects.create_user(username="bob", password="pass123")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )

        notifications = Notification.objects.filter(user=self.receiver, message=msg)
        self.assertEqual(notifications.count(), 1)
