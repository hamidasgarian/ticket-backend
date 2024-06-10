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
    
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('qr_code_id', 'qr_code')

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        # Generate qr_code_id based on instance primary key (pk)
        qr_code_id = f"qr_{instance.pk}"
        instance.qr_code_id = qr_code_id
        print (instance.qr_code_id)

        # Generate QR code with the qr_code_id
        qr_data = f"{qr_code_id}"
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
        img_name = f'qr_code_{instance.pk}.png'

        instance.qr_code.save(img_name, File(buffer), save=False)

        # Save the instance again to update the qr_code_id and qr_code fields
        instance.save()

        return instance

