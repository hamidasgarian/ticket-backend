import json
import inspect
import os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.conf import settings

from melipayamak import Api

def send_sms(phone_number, verify_code):
    username = '09138162670'
    password = '40d92965-46da-4499-b0e6-e0ece9de8fe2'
    provider_phone_number = '50002710062670'
    api = Api(username,password)
    sms = api.sms()
    to = phone_number
    _from = provider_phone_number
    text = verify_code
    response = sms.send(to,_from,text)
    print(response)

send_sms('09374848660','8585')