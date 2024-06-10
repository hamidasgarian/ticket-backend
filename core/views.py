from rest_framework.views import APIView
from rest_framework.response import Response

class HelloWorldView(APIView):
    def get(self, request):
        data = {"message": "Hello, World!"}
        return Response(data)