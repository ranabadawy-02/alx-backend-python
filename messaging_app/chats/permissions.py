from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only allow participants of a conversation to access messages
    or the conversation itself.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be:
        - Conversation instance → check participants
        - Message instance → check message.conversation.participants
        """
        # Conversation object
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Message object
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
