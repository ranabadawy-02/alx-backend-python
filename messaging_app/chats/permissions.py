from rest_framework.permissions import BasePermission

class IsOwnerOfChat(BasePermission):
    """
    Object-level permission: users can access only chats
    where they are a participant.
    """

    def has_object_permission(self, request, view, obj):
        # obj = Chat or Message instance
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        if hasattr(obj, "sender"):
            return obj.sender == request.user
        return False
