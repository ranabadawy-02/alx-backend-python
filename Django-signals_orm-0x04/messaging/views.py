from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    """
    Deletes the currently logged-in user's account.
    """
    user = request.user
    logout(request)  # log them out before deletion
    user.delete()
    return redirect("/")  # redirect to homepage after deletion
