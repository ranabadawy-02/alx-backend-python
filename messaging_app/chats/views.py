from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .permissions import IsParticipantOfConversation


# -----------------------------
# Conversation ViewSet
# -----------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # ✅ Add IsAuthenticated
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response({"error": "Conversation must have at least one participant"},
                            status=status.HTTP_400_BAD_REQUEST)
        participants = User.objects.filter(user_id__in=participant_ids)
        if request.user not in participants:
            participants = list(participants) + [request.user]

        conversation = Conversation.objects.create()
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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # ✅ Add IsAuthenticated
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender_id')
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

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

        # Check if sender is part of the conversation
        if sender not in conversation.participants.all():
            return Response(
                {"error": "Sender is not a participant of the conversation"},
                status=status.HTTP_403_FORBIDDEN  # ✅ Explicit 403
            )

        message = Message.objects.create(sender=sender, conversation=conversation, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
