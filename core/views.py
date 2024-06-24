import json
import inspect
import os
import requests
import random
import uuid
import threading
import time

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from io import BytesIO
from PIL import Image

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


import arabic_reshaper
from bidi.algorithm import get_display

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError


from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.schemas.generators import BaseSchemaGenerator
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.renderers import OpenAPIRenderer
from drf_yasg.inspectors import SwaggerAutoSchema

from .serializers import *
from .models import Ticket as TicketModel
from .pagination import *

from ticket import settings

from core.melipayamak import Api



app_version = 1

def generate_code():
    return str(random.randint(10000, 99999))


def send_sms2(phone_number, verify_code):
    username = settings.SMS_PANEL_USENAME
    password = settings.SMS_PANEL_PASSWORD
    provider_phone_number = settings.SMS_PANEL_PHONE_NUMBER
    api = Api(username,password)
    sms = api.sms()
    to = phone_number
    _from = provider_phone_number
    text = verify_code
    response = sms.send(to,_from,text)
    print(response)


def send_sms(to, text):
    username = "09197705347"
    password = "Fool@dBasa14002021"
    url = "http://api.payamak-panel.com/post/sendsms.ashx"

    payload = {
        "username": username,
        "password": password,
        "to": to,
        "from": "",  # Assuming 'from' parameter should be an empty string
        "text": text
    }

    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def serve_logo(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
        if team.logo_filename:
            file_path = os.path.join(settings.BASE_DIR, 'static', team.logo_filename)
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), content_type='image/png')
        raise Http404("Logo not found.")
    except Team.DoesNotExist:
        raise Http404("Team not found.")


def serve_slider(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'static', filename)
    return FileResponse(open(file_path, 'rb'), content_type='image/png')
    

def check_order_history(seat_owner, match_id):
    return not Ticket.objects.filter(seat_owner=seat_owner, match=match_id).exists()

def check_seat_availibility(ticket_id):
    return not Ticket.objects.filter(ticket_id=ticket_id).exists()
    

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

class user_view(viewsets.ModelViewSet):

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
            print(e)
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


class role_view(viewsets.ModelViewSet):

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


class team_view(viewsets.ModelViewSet):

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated, SisaAdmin]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            err = handle_exception(get_current_class_name(), get_current_action_name())
            return JsonResponse({'ERROR': err[0]}, status=err[1])
        
    @action(detail=False, methods=['get'], url_path='count', url_name='count')
    def count(self, request, *args, **kwargs):
        try:
            team_count = Team.objects.count()
            return JsonResponse({'count': team_count})
        except Exception as e:
            return JsonResponse({'ERROR': str(e)}, status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = TeamSerializer(data=request.data)
            if serializer.is_valid():
                ticket_instance = serializer.save()
                return Response(TeamSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
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


class stadium_view(viewsets.ModelViewSet):

    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
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
            serializer = StadiumSerializer(data=request.data)
            if serializer.is_valid():
                ticket_instance = serializer.save()
                return Response(StadiumSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
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


class capacity_view(viewsets.ModelViewSet):

    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer

    @action(detail=False, methods=['get'], url_path='seat_costs_per_match/(?P<match_id>[^/.]+)/(?P<seat_position>[^/.]+)')
    def seat_costs_per_match(self, request, match_id=None, seat_position=None):
        try:
            capacity = Capacity.objects.get(id=match_id)
            stadium = Stadium.objects.get(id=app_version)
            seat_position = int(seat_position)

            if seat_position in stadium.stadium_seat_category1:
                category = "category1"
            if seat_position in stadium.stadium_seat_category2:
                category = "category2"
            if seat_position in stadium.stadium_seat_category3:
                category = "category3"
            if seat_position in stadium.stadium_seat_category4:
                category = "category4"

            data = {
                'seat_costs_per_position': capacity.seat_costs_per_position[category]
            }
            return Response(data, status=status.HTTP_200_OK)
        except capacity.DoesNotExist:
            return Response({'error': 'capacity not found for the given match ID'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='stadium-capacity/(?P<match_id>[^/.]+)')
    def stadium_capacity(self, request, match_id=None):
        try:
            capacity = Capacity.objects.get(id=match_id)
            data = {
                'all_available_seats': capacity.all_available_seats,
                'all_available_host_seats': capacity.all_available_host_seats,
                'all_available_guest_seats': capacity.all_available_guest_seats
            }
            return Response(data, status=status.HTTP_200_OK)
        except capacity.DoesNotExist:
            return Response({'error': 'capacity not found for the given match ID'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'], url_path='available-seat-per-positions/(?P<match_id>[^/.]+)/(?P<position_number>[^/.]+)/(?P<seat_type>[^/.]+)')
    def available_seat_per_positions(self, request, match_id=None, position_number=None, seat_type=None):
        try:
            capacity = Capacity.objects.get(id=match_id)
            position_number = int(position_number) - 1
            if seat_type == 'host':
                available_seats = capacity.available_seats_per_position_host[position_number]
            elif seat_type == 'guest':
                available_seats = capacity.available_seats_per_position_guest[position_number]
            else:
                return Response({'error': 'Invalid seat type'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                'available_seats_in_position': available_seats
            }
            return Response(data, status=status.HTTP_200_OK)
        except Capacity.DoesNotExist:
            return Response({'error': 'Capacity not found for the given match ID'}, status=status.HTTP_404_NOT_FOUND)
        except IndexError:
            return Response({'error': 'Invalid position number'}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['get'], url_path='available-seat-per-rows/(?P<match_id>[^/.]+)/(?P<position_number>[^/.]+)/(?P<row_number>[^/.]+)/(?P<seat_type>[^/.]+)')
    def available_seat_per_rows(self, request, match_id=None, position_number=None, row_number=None, seat_type=None):
        try:
            capacity = Capacity.objects.get(id=match_id)
            position_number = int(position_number) - 1 
            row_number = int(row_number) - 1
            if seat_type == 'host':
                if position_number >= len(capacity.available_seats_per_position_host):
                    return Response({'error': 'Invalid position number for host'}, status=status.HTTP_400_BAD_REQUEST)
                available_seats = capacity.available_seats_per_position_host[position_number] // capacity.rows_per_position
            elif seat_type == 'guest':
                if position_number >= len(capacity.available_seats_per_position_guest):
                    return Response({'error': 'Invalid position number for guest'}, status=status.HTTP_400_BAD_REQUEST)
                available_seats = capacity.available_seats_per_position_guest[position_number] // capacity.rows_per_position
            else:
                return Response({'error': 'Invalid seat type'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                'available_seats_in_row': available_seats
            }
            return Response(data, status=status.HTTP_200_OK)
        except Capacity.DoesNotExist:
            return Response({'error': 'Capacity not found for the given match ID'}, status=status.HTTP_404_NOT_FOUND)
        except IndexError:
            return Response({'error': 'Invalid position number or row number'}, status=status.HTTP_400_BAD_REQUEST)




class match_view(viewsets.ModelViewSet):

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    # renderer_classes = [CustomOpenAPIRenderer]
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
            serializer = MatchSerializer(data=request.data)
            if serializer.is_valid():
                ticket_instance = serializer.save()
                return Response(MatchSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
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

        
class tools(viewsets.ViewSet):
    @swagger_auto_schema(
            method='post',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'mobile': openapi.Schema(type=openapi.TYPE_STRING)
                
                },
                required=['mobile']
            )
        )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def generate_verification_code(self, request):
        request_data = json.loads(request.body)
        mobile = request_data.get('mobile')
        code = generate_code()
        cache.set(f'verification_code_{mobile}', code, timeout=300)  # Store the code for 5 minutes
        # Send the code to the user via email or any other method here.
        send_sms(mobile, code)
        return HttpResponse('Successfully sent the code')


    @swagger_auto_schema(
            method='post',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                    'code': openapi.Schema(type=openapi.TYPE_STRING)
                
                },
                required=['mobile', 'code']
            )
        )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def verify_code(self, request):

        def generate_jwt_token(mobile_number):
            refresh = RefreshToken()
            refresh['mobile'] = mobile_number
            access_token = str(refresh.access_token)
            return access_token


        request_data = json.loads(request.body)
        input_code = request_data.get('code')
        user_id = request_data.get('mobile')
        cached_code = cache.get(f'verification_code_{user_id}')
        if cached_code and cached_code == input_code:
            access_token = generate_jwt_token(user_id)

            admin = Admins.objects.get(id=app_version)
            user_is_admin = any(user_id in element for element in admin.admin_phones)

            if user_is_admin:
                access_level = "admin"
            else:
                access_level = "user"


            return JsonResponse({'access_token': access_token,
                                 'access_level': access_level}, status=200)
        else:
            return HttpResponse('Invalid or expired code.', status=401)

            

    
class ticket_view(viewsets.ViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get_sold_tickets_in_specific_row/(?P<match_id>[^/.]+)/(?P<seat_position>[^/.]+)/(?P<seat_row>[^/.]+)')
    def get_sold_tickets_in_specific_row(self, request, match_id=None, seat_position=None, seat_row=None):
        try:
            tickets = Ticket.objects.filter(
                match=match_id,
                seat_row=seat_row,
                seat_position=seat_position,
                seat_availibility=False
            )
            if not tickets.exists():
                raise ObjectDoesNotExist("No tickets found for the given criteria.")
            
            ticket_seat_numbers = [ticket.seat_number for ticket in tickets]
            return Response(ticket_seat_numbers)
        except ObjectDoesNotExist as e:
            print(f"Error: {e}")
            return Response({'error': str(e)}, status=404)
        except DatabaseError as e:
            print(f"Database error: {e}")
            return Response({'error': str(e)}, status=500)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return Response({'error': str(e)}, status=500)



    @action(detail=False, methods=['get'], url_path='ticket_sold_by_match/(?P<match_id>[^/.]+)')
    def ticket_sold_by_match(self, request, match_id=None):
        try:
            
            match = Match.objects.get(id=match_id)
            tickets = Ticket.objects.filter(match_id=match.id)

            ticket_sold_by_match = {
                match.match_name: list(tickets.values_list('ticket_id', flat=True))
                
            }


            return JsonResponse(ticket_sold_by_match, status=status.HTTP_200_OK)
        except Match.DoesNotExist:
            return Response({"detail": "Match not found."}, status=status.HTTP_404_NOT_FOUND)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

    
    @action(detail=False, methods=['get'], url_path='ticket_count_per_match')
    @csrf_exempt
    def ticket_count_per_match(self, request):
        try:
            
            matches = Match.objects.all()

            ticket_count_per_match = {
                match.match_name: Ticket.objects.filter(match_id=match.id).count()
                for match in matches
            }


            return JsonResponse(ticket_count_per_match, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
    @action(detail=False, methods=['get'], url_path='ticket_count_per_match_detail')
    @csrf_exempt
    def ticket_count_per_match_detail(self, request):
        try:
            
            matches = Match.objects.all()

            ticket_count_per_match = {
                match.match_name: list(Ticket.objects.filter(match_id=match.id).values_list('ticket_id', flat=True))
                for match in matches
            }


            return JsonResponse(ticket_count_per_match, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
        

    @action(detail=False, methods=['get'])
    @csrf_exempt
    def ticket_costs(self, request):
        try:
            
            stadium = Stadium.objects.get(id=app_version)
            cost = Capacity.objects.get(id=app_version)
            ticket_costs = {
                tuple(stadium.stadium_seat_category1): cost.seat_costs_per_position["category1"],
                tuple(stadium.stadium_seat_category2): cost.seat_costs_per_position["category2"],
                tuple(stadium.stadium_seat_category3): cost.seat_costs_per_position["category3"],
                tuple(stadium.stadium_seat_category4): cost.seat_costs_per_position["category4"]
            }
            ticket_costs_json = [{"seat_position": list(k), "seat_cost": v} for k, v in ticket_costs.items()]


            return JsonResponse(ticket_costs_json, status=status.HTTP_200_OK, safe=False)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)


    

    @action(detail=True, methods=['GET'])
    @csrf_exempt
    def detail_ticket(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
        


    @swagger_auto_schema(method='get')
    @action(detail=False, methods=['get'])
    @csrf_exempt
    def list_ticket(self, request):
        tickets = Ticket.objects.all()  
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
        
                'mobile': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['mobile']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def user_order_history(self, request):


        request_data = json.loads(request.body)
        mobile = request_data.get('mobile')
        tickets = Ticket.get_by_mobile(mobile)
        serializer = TicketSerializer(tickets, many=True)
        # tickets_data = list(tickets.values('id', 'mobile', 'seat_owner', 'match_id'))  # Customize the fields you want to return
        return JsonResponse(serializer.data, safe=False)
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
        
                'match_id': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['match_id']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def get_unavailable_seats(self, request):


        request_data = json.loads(request.body)
        match_id = request_data.get('match_id')
        seats = Ticket.get_unavailable_seats_by_match(match_id)
        seats_list = list(seats)
        # serializer = TicketSerializer(tickets, many=True)
        # tickets_data = list(tickets.values('id', 'mobile', 'seat_owner', 'match_id'))  # Customize the fields you want to return
        return JsonResponse(seats_list, safe=False)
    

    


    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
        
                'mobile': openapi.Schema(type=openapi.TYPE_STRING),
                'match': openapi.Schema(type=openapi.TYPE_INTEGER),
                'seat_type': openapi.Schema(type=openapi.TYPE_STRING),
                'seat_position': openapi.Schema(type=openapi.TYPE_STRING),
                'seat_row': openapi.Schema(type=openapi.TYPE_STRING),
                'seat_owners': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT))
            },
            required=['mobile', 'seat_owners', 'match', 'seat_type', 'seat_position', 'seat_row', 'seat_numbers']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def buy_ticket(self, request):


        request_data = json.loads(request.body)
        mobile = request_data.get('mobile')
        seat_owners = request_data.get('seat_owners')
        match_id = request_data.get('match')
        seat_type = request_data.get('seat_type')
        seat_position = request_data.get('seat_position')
        seat_row = request_data.get('seat_row')
        seat_owners = request_data.get('seat_owners')

        
        match_obj = Match.objects.get(id=match_id)
        capacity_obj = Capacity.objects.get(id=match_id)
        stadium_obj = Stadium.objects.get(id=app_version)

        successful_tickets = []
        errors = []

        for seat_owner in seat_owners:
            national_id = seat_owner["national_id"]
            last_two_digits = national_id[-2:]
            hint = int(last_two_digits[0]) + int(last_two_digits[1])

            seat_number = seat_owner["seat_number"]
            ticket_id = f"{national_id}_{match_obj.match_number}_{seat_position}_{seat_row}_{seat_number}_{hint}"
            
            if check_order_history(national_id, match_id) and check_seat_availibility(ticket_id):
                
                capacity_obj.sell_ticket(match_id, int(seat_position), int(seat_row), seat_type)
                
                ticket_instance = Ticket.objects.create(
                    mobile=mobile,
                    seat_owner=national_id,
                    match=match_obj,
                    stadium=stadium_obj,
                    seat_row=seat_row,
                    seat_position=seat_position,
                    seat_number=seat_number,
                    seat_type=seat_type,
                    seat_costs=150000,
                    seat_availibility=False,
                    ticket_id=ticket_id

                )

                successful_tickets.append(ticket_id)

            else:
                errors.append({"seat_owner": seat_owner["national_id"], "detail": "Seat or match already booked."})

        if successful_tickets:
            return Response({'message': 'successful', 'tickets': successful_tickets}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Seat or match already booked for all entries.", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ticket_id': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['ticket_id']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def generate_ticket_file(self, request):
        request_data = json.loads(request.body)
        ticket_id = request_data.get('ticket_id')

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        real_ticket_id = ticket.ticket_id
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(real_ticket_id)
        qr.make(fit=True)

        img = qr.make_image(image_factory=StyledPilImage, module_drawer=GappedSquareModuleDrawer(), color_mask=RadialGradiantColorMask(back_color=(255,255,255), edge_color=(253,200,0), center_color=(0,0,0)))

        logo_display = Image.open("static/سپاهان_logo.png")
        logo_display = logo_display.resize((60, 60), Image.LANCZOS)

        pos = (
            (img.size[0] - logo_display.size[0]) // 2,
            (img.size[1] - logo_display.size[1]) // 2
        )
        img.paste(logo_display, pos, logo_display)

        pdf_path = os.path.join(settings.MEDIA_ROOT, 'tickets')
        os.makedirs(pdf_path, exist_ok=True)
        filename = f"{uuid.uuid4()}.pdf"
        full_path = os.path.join(pdf_path, filename)

        content_width = 200  # Width of QR code image
        content_height = 300  # Estimated height needed for text
        margin = 2 * cm
        page_width = content_width + 2 * margin
        page_height = content_height + 2 * margin

        pdf = canvas.Canvas(full_path, pagesize=(page_width, page_height))
        width, height = page_width, page_height

        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        pdfmetrics.registerFont(TTFont('Persian', 'static/Vazir.ttf'))
        pdf.setFont("Persian", 12)

        tag = get_display(arabic_reshaper.reshape(f"سامانه آنلاین فروش بلیط باشگاه سپاهان"))
        match_name = get_display(arabic_reshaper.reshape(f"                 {ticket.match.match_name}"))
        match_time = get_display(arabic_reshaper.reshape(f"تاریخ : {ticket.match.match_date}     ساعت : {ticket.match.match_time} "))
        seat_owner = get_display(arabic_reshaper.reshape(f"کدملی : {ticket.seat_owner}"))
        seat_type_and_position = get_display(arabic_reshaper.reshape(f"جایگاه : {ticket.seat_type}                      سکو: {ticket.seat_position}"))
        seat_row_and_number = get_display(arabic_reshaper.reshape(f"ردیف : {ticket.seat_row}                          صندلی: {ticket.seat_number}"))

        pdf.drawRightString(width - margin, height - content_width - 25 , tag)
        pdf.drawImage(ImageReader(img_buffer), x=(width - content_width) / 2, y=content_height - 100, width=content_width, height=content_width)
        pdf.drawRightString(width - margin, height - content_width - margin - 10, match_name)
        pdf.drawRightString(width - margin, height - content_width - margin - 35, match_time)
        pdf.drawRightString(width - margin, height - content_width - margin - 65, seat_owner)
        pdf.drawRightString(width - margin, height - content_width - margin - 90, seat_type_and_position)
        pdf.drawRightString(width - margin, height - content_width - margin - 110, seat_row_and_number)

        pdf.showPage()
        pdf.save()

        download_link = request.build_absolute_uri(settings.MEDIA_URL + 'tickets/' + filename)
        return Response({'download_link': download_link}, status=status.HTTP_201_CREATED)        



    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
        
                'ticket_id': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['ticket_id']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def verify_ticket(self, request):
        
        try:
            request_data = json.loads(request.body)
            ticket_id = request_data.get('ticket_id')
            try:
                ticket = Ticket.objects.get(ticket_id=ticket_id)
            except Ticket.DoesNotExist:
                return JsonResponse({"detail": "Ticket is fake."}, status=status.HTTP_404_NOT_FOUND)
            

            if ticket.ticket_used == 0:
                ticket.ticket_used = 1
                ticket.save()
                return JsonResponse({"detail": "Ticket is verified."}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"detail": "Ticket not verified."}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        

# sample json
# {
#   "mobile": "09374848660",
#   "match": 1,
#   "seat_type": "host",
#   "seat_position": "1",
#   "seat_row": "1",
#   "seat_owners": [
#     {"national_id": "0010857222", "seat_number": "11"}, {"national_id": "0010857223", "seat_number": "12"}, {"national_id": "0010857224", "seat_number": "13"}
#   ]
# }