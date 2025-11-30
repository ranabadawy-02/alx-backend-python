from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message

def unread_inbox(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, "messaging/unread_inbox.html", {"messages": unread_messages})


@login_required
def delete_user(request):
    """
    Deletes the currently logged-in user's account.
    """
    user = request.user
    logout(request)  # log them out before deletion
    user.delete()
    return redirect("/")  # redirect to homepage after deletion

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message


@login_required
def user_conversations(request):
    """
    Fetch all conversations for the logged-in user,
    optimized using select_related and prefetch_related.
    """

    messages = (
        Message.objects
        .filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    )

    # Apply ORM optimizations
    messages = messages.select_related("sender", "receiver").prefetch_related("replies")

    context = {
        "messages": messages
    }
    return render(request, "messaging/conversations.html", context)
