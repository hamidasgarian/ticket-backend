import json
import inspect
import os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.conf import settings


from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.schemas.generators import BaseSchemaGenerator
from rest_framework import viewsets, permissions


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.renderers import OpenAPIRenderer
from drf_yasg.inspectors import SwaggerAutoSchema

from .serializers import *
from .models import Ticket as TicketModel
from ticket import settings

from melipayamak import Api

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
    

def check_order_history(user, match_id):
    return not Ticket.objects.filter(user=user, match_id=match_id).exists()

def check_seat_availibility(global_seat_uique_id):
    return not Ticket.objects.filter(global_seat_uique_id=global_seat_uique_id).exists()
    

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


class ticket_view(viewsets.ViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

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
                'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                'match': openapi.Schema(type=openapi.TYPE_INTEGER),
                'host_team': openapi.Schema(type=openapi.TYPE_INTEGER),
                'guest_team': openapi.Schema(type=openapi.TYPE_INTEGER),
                'stadium_name': openapi.Schema(type=openapi.TYPE_INTEGER),
                'stadium_row': openapi.Schema(type=openapi.TYPE_STRING),
                'stadium_position': openapi.Schema(type=openapi.TYPE_STRING),
                'stadium_seat': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['user', 'match', 'host_team', 'guest_team', 'stadium_name', 'stadium_row', 'stadium_position', 'stadium_seat']
        )
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def buy_ticket(self, request):


        request_data = json.loads(request.body)
        user_id = request_data.get('user')
        match_id = request_data.get('match')
        host_team_id = request_data.get('host_team')
        guest_team_id = request_data.get('guest_team')
        stadium_name = request_data.get('stadium_name')
        stadium_row = request_data.get('stadium_row')
        stadium_position = request_data.get('stadium_position')
        stadium_seat = request_data.get('stadium_seat')

        
        user_obj = User.objects.get(id=user_id)
        match_obj = Match.objects.get(id=match_id)
        host_team_obj = Team.objects.get(id=user_id)
        guest_team_obj = Team.objects.get(id=user_id)
        stadium_obj = Stadium.objects.get(id=user_id)

        ticket_id = f"{user_obj.national_id}_{match_obj.match_id}_{stadium_name}_{stadium_row}_{stadium_position}_{stadium_seat}"
        global_seat_uique_id = f"{match_obj.match_id}{stadium_name}{stadium_row}{stadium_position}{stadium_seat}"

        qr_code_id = f"qr_{ticket_id}"
        if check_order_history(user_id, match_id) and check_seat_availibility(global_seat_uique_id):

            ticket_instance = Ticket.objects.create(
                user=user_obj,
                match=match_obj,
                host_team=host_team_obj,
                guest_team=guest_team_obj,
                stadium_name=stadium_obj,
                stadium_row=stadium_row,
                stadium_position=stadium_position,
                stadium_seat=stadium_seat,
                qr_code_id=qr_code_id,
                global_seat_uique_id=global_seat_uique_id,
                ticket_id=ticket_id
            )

            qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,)
            qr.add_data(qr_code_id)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_name = f'{qr_code_id}.png'
            ticket_instance.qr_code.save(img_name, ContentFile(buffer.getvalue()), save=True)

            return Response({'message': 'successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Seat or match already booked."}, status=status.HTTP_400_BAD_REQUEST)
        
    def send_sms(phone_number, verify_code):
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
    
    
    
    
    # def buy_ticket(self, request):
    #     request_data = json.loads(request.body)
    #     user = request_data.get('user')
    #     match = request_data.get('match')
    #     host_team = request_data.get('host_team')
    #     guest_team = request_data.get('guest_team')
    #     stadium_name = request_data.get('stadium_name')
    #     stadium_row = request_data.get('stadium_row')
    #     stadium_position = request_data.get('stadium_position')
    #     stadium_seat = request_data.get('stadium_seat')
        

    #     user_obj = User.objects.get(id=1)
    #     national_id = user_obj.national_id
    #     match_obj = Match.objects.get(id=match)
    #     match_id = match_obj.match_id
    #     ticket_id = f"{national_id}_{match_id}_{stadium_name}_{stadium_row}_{stadium_position}_{stadium_seat}"

    #     qr_code_id=f"qr_{ticket_id}"

    #     ticket_instance = {
    #             'user': user,
    #             'match': match,
    #             'host_team': host_team,
    #             'guest_team': guest_team,
    #             'stadium_name': stadium_name,
    #             'stadium_row': stadium_row,
    #             'stadium_position': stadium_position,
    #             'stadium_seat': stadium_seat,
    #             'qr_code_id': qr_code_id,
    #             'ticket_id': ticket_id

    #         }
        


    #     qr_data = f"{qr_code_id}"
    #     qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,)
    #     qr.add_data(qr_data)
    #     qr.make(fit=True)

    #     img = qr.make_image(fill='black', back_color='white')

    #     buffer = BytesIO()
    #     img.save(buffer, format="PNG")
    #     img_name = f'{qr_code_id}.png'

    #     qr.qr_code.save(img_name, File(buffer), save=False)


    #     created_record = create_ticket(ticket_instance)

    #     if created_record:
    #         return JsonResponse({'message': 'successful'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return JsonResponse({'message': 'unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
    #         # print("Seat or match already booked.")
        






        
        # serializer = TicketSerializer(data=request.data)
        
        # if serializer.is_valid():
            
        #     print('777777')
        #     request_data = json.loads(request.body)
        #     print(request_data)
        #     print('777777')
        #     if check_order_history(request.user, request.data.get('match_id')) and check_seat_availibility(request.data.get('ticket_id')):
        #         ticket_instance = serializer.save()
        #         return Response(TicketSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response({"detail": "Seat or match already booked."}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
            #     ticket_instance = serializer.save(user=request.user)
            #     return Response(TicketSerializer(ticket_instance).data, status=status.HTTP_201_CREATED)
            # else:
            #     return Response({"detail": "Seat or match already booked."}, status=status.HTTP_400_BAD_REQUEST)
        

    
