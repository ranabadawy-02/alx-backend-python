from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# -----------------------------
# Conversation ViewSet
# -----------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a list of participant IDs.
        Example payload: {"participants": ["uuid1", "uuid2"]}
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response(
                {"error": "Conversation must have at least one participant"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create conversation
        conversation = Conversation.objects.create()
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------
# Message ViewSet
# -----------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message in an existing conversation.
        Example payload: {"sender_id": "uuid1", "conversation_id": "uuid2", "message_body": "Hello"}
        """
        sender_id = request.data.get('sender_id')
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        # Validate input
        if not sender_id or not conversation_id or not message_body:
            return Response(
                {"error": "sender_id, conversation_id, and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sender = User.objects.get(user_id=sender_id)
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"}, status=status.HTTP_404_NOT_FOUND)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
