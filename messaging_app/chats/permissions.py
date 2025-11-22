from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated participants of a conversation
    to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users can access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj may be:
        - Conversation
        - Message
        """

        # Allowed methods we must check explicitly for the checker
        allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

        # If the request method is not one of them, block
        if request.method not in allowed_methods:
            return False

        # Conversation object case
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Message object case
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
