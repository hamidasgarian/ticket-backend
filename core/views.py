from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import inspect

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from ticket import settings

def handle_exception(class_name, action_name):
    if settings.DEBUG:
        error_message = f"You have an error in action: {class_name}.{action_name}"
        result_status_code = 485
    else:
        error_message = "Internal Server Error"
        result_status_code = 500
    return error_message, result_status_code

def get_current_action_name():
    frame = inspect.currentframe().f_back
    action_name = inspect.getframeinfo(frame).function
    return action_name


def get_current_class_name():
    frame = inspect.currentframe().f_back
    class_name = frame.f_locals.get('self').__class__.__name__
    return class_name



class User(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, SisaAdmin]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user_instance = serializer.save()
                return Response(UserSerializer(user_instance).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])


class Role(viewsets.ModelViewSet):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, SisaAdmin]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def create(self, request, *args, **kwargs):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                ticket_instance = serializer.save()
                return Response(RoleSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])


    
class Ticket(viewsets.ViewSet):

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
        
    @swagger_auto_schema(
    method='get'
    )
    @action(detail=False, methods=['get'])
    @csrf_exempt

    def list(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            return Response(TicketSerializer(ticket_instance).data, status=status.HTTP_200_)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
