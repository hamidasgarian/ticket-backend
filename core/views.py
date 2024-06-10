from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import *

class CreateUser(viewsets.ViewSet):
    @swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name' :  openapi.Schema(type=openapi.TYPE_STRING),
            'last_name' :  openapi.Schema(type=openapi.TYPE_STRING),
            'phone_number' :  openapi.Schema(type=openapi.TYPE_STRING),
            'national_id' :  openapi.Schema(type=openapi.TYPE_STRING),
            'birthday' :  openapi.Schema(type=openapi.TYPE_STRING,example="1990-01-01"),
            'role' :  openapi.Schema(type=openapi.TYPE_INTEGER)
        },
        required=['first_name','last_name','phone_number','national_id','birthday','role']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_instance = serializer.save()
            return Response(UserSerializer(user_instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateRole(viewsets.ViewSet):

    @swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'role_name' :  openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['role_name']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            role_instance = serializer.save()
            return Response(RoleSerializer(role_instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateTicket(viewsets.ViewSet):

    @swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user' :  openapi.Schema(type=openapi.TYPE_INTEGER),
            'host_team' :  openapi.Schema(type=openapi.TYPE_INTEGER),
            'guest_team' :  openapi.Schema(type=openapi.TYPE_INTEGER),
            'stadium_name' :  openapi.Schema(type=openapi.TYPE_INTEGER),
            'stadium_row' :  openapi.Schema(type=openapi.TYPE_INTEGER),
            'stadium_position' :  openapi.Schema(type=openapi.TYPE_INTEGER),
            'stadium_seat' :  openapi.Schema(type=openapi.TYPE_INTEGER),
            'match_date' :  openapi.Schema(type=openapi.TYPE_STRING,example="1990-01-01")
        },
        required=['user','host_team','guest_team','stadium_name','match_date','stadium_row','stadium_position','stadium_seat']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket_instance = serializer.save()
            return Response(TicketSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
