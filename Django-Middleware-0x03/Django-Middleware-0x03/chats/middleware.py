from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    """
    Middleware that allows only users with role 'admin' or 'moderator'
    to access specific chat actions.
    """

    ALLOWED_ROLES = ['admin', 'moderator']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip check if user is anonymous
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in.")

        # Assume user has a 'role' attribute (admin, moderator, user)
        user_role = getattr(request.user, 'role', 'user')

        if user_role not in self.ALLOWED_ROLES:
            return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)
