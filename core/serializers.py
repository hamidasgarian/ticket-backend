from rest_framework import serializers
from .models import *
import qrcode
from io import BytesIO


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
    
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def save(self, *args, **kwargs):
        qr_data = f"Ticket for {self.user} at {self.place} on {self.buy_date}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_name = f'qr_code_{self.pk}.png'

        self.qr_code.save(img_name, File(buffer), save=False)

        super().save(*args, **kwargs)

def ticket(data):
    serializer = TicketSerializer(data=data)

    if serializer.is_valid():
        ticket_instance = serializer.save()
        return ticket_instance
    else:
        errors = serializer.errors
        print(errors)
        return errors


