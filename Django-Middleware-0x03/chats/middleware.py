from datetime import datetime
import logging

class RequestLoggingMiddleware:
    """
    Middleware that logs every request with timestamp, user, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Configure logger (writes to requests.log)
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        # Continue the request
        response = self.get_response(request)
        return response

from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Blocks access to the chat outside allowed hours (6 PM – 9 PM)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        # Allowed hours: 6 PM (18:00) to 9 PM (21:00)
        from datetime import time
        start_time = time(18, 0)   # 6 PM
        end_time = time(21, 0)     # 9 PM

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access to chat is restricted at this time.")

        return self.get_response(request)
