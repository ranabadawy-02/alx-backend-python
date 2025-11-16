import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# User Model
# -----------------------------
class User(AbstractUser):
    # Replace default id with UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Additional fields
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password_hash = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    # Enum field for role
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # username required by AbstractUser

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# -----------------------------
# Conversation Model
# -----------------------------
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# -----------------------------
# Message Model
# -----------------------------
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} by {self.sender.email}"
