import requests
import random
import os
import inspect

from django.http import FileResponse, Http404

from ticket import settings
from core.models import *
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
    # print(response)


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

def calculate_seat_cost_by_seat_position(match_id, seat_position):
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

    
    return capacity.seat_costs_per_position[category]


def calculate_sold_seat_per_match(match_id, seat_position):
    cap_obj = Capacity.objects.get(id=match_id)
    cap = cap_obj.stadium_audience_structure

    ticket_count_per_match = Ticket.objects.filter(
                match=match_id,
                seat_position=seat_position
            ).count()
    
    return ticket_count_per_match

def calculate_sold_seat_per_row(match_id, seat_position, seat_row, seat_type):
    cap_obj = Capacity.objects.get(id=match_id)
    cap = cap_obj.stadium_audience_structure

    ticket_count_per_row = Ticket.objects.filter(
                match=match_id,
                seat_row=seat_row,
                seat_type=seat_type,
                seat_position=seat_position
            ).count()
    
    return ticket_count_per_row




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

