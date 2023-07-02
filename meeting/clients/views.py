from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from services.email_service import EmailMessage, CommonMatchMessage, send_all_mails
from .serializers import ClientRegisterSerializer
from .models import Client, ClientMatch
from .filters import ClientFilter


class CreationView(APIView):
    def post(self, request: Request):
        client = ClientRegisterSerializer(data=request.data)
        if client.is_valid(raise_exception=True):
            client.save()
            return Response({'message': client.data})


class ClientMath(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, client_id=None):
        matched_client = Client.objects.filter(id=client_id).first()
        if request.user.id == client_id or not matched_client:
            response = Response({'message': 'invalid user id'})
            response.status_code = 404
            return response

        response = {'message': 'match added', 'is_mutual': False}
        try:
            match = ClientMatch(from_client_id=request.user,
                                to_client_id=matched_client)
            match.save()
        except IntegrityError:
            response['message'] = 'match already add'

        if ClientMatch.objects.filter(from_client_id=client_id, to_client_id_id=request.user.id):
            response['is_mutual'] = True
            response['detail'] = {'client_email': matched_client.email}
            # Создаем email сообщения
            message_to_matched_client = EmailMessage(message_object=CommonMatchMessage(
                client_first_name=request.user.first_name,
                client_email=request.user.email),
                message_recipient=matched_client.email)
            message_to_request_client = EmailMessage(message_object=CommonMatchMessage(
                client_first_name=matched_client.first_name,
                client_email=matched_client.email),
                message_recipient=request.user.email)

            # Отправляем созданные сообщения
            send_all_mails([message_to_request_client, message_to_matched_client])

        return Response(response)


class ClientList(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegisterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClientFilter

    def get(self, request: Request, *args, **kwargs):
        # Проверка, что пользователь указал параметр distance и он не авторизован
        if 'distance' in request.query_params and not request.auth:
            response = Response({'message': 'Filter by distance param only for authorized users'})
            response.status_code = 404
            return response
        # Если пользователь авторизован убираем его из выборки
        if request.auth:
            self.queryset = self.queryset.exclude(id=request.user.id)
        return super().get(request, *args, **kwargs)
