from rest_framework import serializers
from .models import *
import qrcode
from io import BytesIO
from django.core.files import File




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


def create_user(data):
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        user_instance = serializer.save()
        return user_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

def role(data):
    serializer = RoleSerializer(data=data)

    if serializer.is_valid():
        role_instance = serializer.save()
        return role_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

def team(data):
    serializer = TeamSerializer(data=data)

    if serializer.is_valid():
        team_instance = serializer.save()
        return team_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['match_name'].example = 'sepahan-zobahan'
    #     self.fields['match_id'].example = '1000'
    #     self.fields['match_date'].example = '1403-01-15'
    #     self.fields['match_time'].example = '14:30:00'
    #     self.fields['match_price'].example = '150000'

def match(data):
    serializer = MatchSerializer(data=data)

    if serializer.is_valid():
        match_instance = serializer.save()
        return match_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'

def stadium(data):
    serializer = StadiumSerializer(data=data)

    if serializer.is_valid():
        stadium_instance = serializer.save()
        return stadium_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors
    
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

def create_ticket(data):
    serializer = TicketSerializer(data=data)

    if serializer.is_valid():
        scan_instance = serializer.save()
        return scan_instance
    else:
        errors = serializer.errors
        print(errors)
        return None


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

        
# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = '__all__'
#         read_only_fields = ('qr_code_id', 'qr_code', 'ticket_id')

#     def save(self, *args, **kwargs):
#         stadium_name = self.validated_data.get('stadium_name')
#         stadium_row = self.validated_data.get('stadium_row')
#         stadium_position = self.validated_data.get('stadium_position')
#         stadium_seat = self.validated_data.get('stadium_seat')
#         national_id = self.validated_data.get('user')
#         # match_id = self.validated_data.get('match')
#         match = self.validated_data.get('match')
#         user = self.validated_data.get('user')
#         match_id = match.match_id
#         national_id = user.national_id
        
#         ticket_id = f"{national_id}_{match_id}_{stadium_name}_{stadium_row}_{stadium_position}_{stadium_seat}"
    
#         self.validated_data['ticket_id'] = ticket_id

        

        

#         instance = super().save(*args, **kwargs)

#         qr_code_id = f"qr_{instance.pk}"
#         instance.qr_code_id = qr_code_id

#         qr_data = f"{qr_code_id}"
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(qr_data)
#         qr.make(fit=True)

#         img = qr.make_image(fill='black', back_color='white')

#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         img_name = f'qr_code_{instance.pk}.png'

#         instance.qr_code.save(img_name, File(buffer), save=False)

#         instance.save()

#         return instance