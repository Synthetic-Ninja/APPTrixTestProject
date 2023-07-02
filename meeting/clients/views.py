from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .serializers import ClientRegisterSerializer


class CreationView(APIView):
    def post(self, request: Request):
        client = ClientRegisterSerializer(data=request.data)
        if client.is_valid(raise_exception=True):
            client.save()
            return Response({'message': client.data})
