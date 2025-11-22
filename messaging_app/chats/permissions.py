from rest_framework import permissions

class IsOwnerOfChat(permissions.BasePermission):
    """
    Allow access only to users who own the chat or the message.
    """

    def has_object_permission(self, request, view, obj):
        # If obj is a Chat → user must be in participants
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If obj is a Message → user must be the sender or a participant in the chat
        if hasattr(obj, "sender"):
            return obj.sender == request.user or request.user in obj.chat.participants.all()

        return False
