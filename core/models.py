from django.db import models
from django.core import validators
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.files import File
import qrcode
from io import BytesIO

def only_digits_validator(value):
    if not value.isdigit():
        raise ValidationError('This field should contain only digits.')

class Role(models.Model):
    name = models.CharField(max_length=50)

    def str(self):
        return self.name
    
class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=11, blank=False, validators=[MinLengthValidator(11)],unique=True)
    national_id = models.CharField(max_length=10, blank=False, validators=[MinLengthValidator(10),only_digits_validator],unique=True)
    birthday = models.DateField(null=True, blank=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Stadium(models.Model):
    stadium_name = models.CharField(max_length=50, blank=False)
    stadium_row = models.ForeignKey(Pl, on_delete=models.CASCADE)
    stadium_position = models.ForeignKey(Role, on_delete=models.CASCADE)
    stadium_seat =  models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.place_name

class Team(models.Model):
    name = models.CharField(max_length=50, blank=False)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='host_team')
    guest_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='guest_team')
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE,  related_name='stadium')
    buy_date = models.DateField(auto_now=True, blank=False)
    match_date = models.DateTimeField(null=True, blank=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=False)
    qr_code_id = models.IntegerField(blank=False, blank=False)
    is_used = models.BooleanField(default=False, blank=False)
    state = models.BooleanField(default=False, blank=False)
    
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

    def __str__(self):
        return f"Ticket for {self.user} to {self.place} on {self.buy_date}"
