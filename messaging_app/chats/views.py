from rest_framework.views import APIView
from rest_framework.response import Response

# Example placeholder API view
class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})
