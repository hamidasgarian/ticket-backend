from django.db import models
from django.core import validators
from django.core.validators import MinLengthValidator,MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError
from django.core.files import File

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

    def __str__(self):
        return self.place_name

class Team(models.Model):
    name = models.CharField(max_length=50, blank=False)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='host_team')
    guest_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='guest_team')
    stadium_name = models.ForeignKey(Stadium, on_delete=models.CASCADE,  related_name='stadium')
    stadium_row = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)])
    stadium_position = models.IntegerField(validators=[MaxValueValidator(100000),MinValueValidator(0)])
    stadium_seat =  models.IntegerField(validators=[MaxValueValidator(100000),MinValueValidator(0)])
    buy_date = models.DateField(auto_now=True, blank=False)
    match_date = models.DateTimeField(null=True, blank=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)
    qr_code_id = models.CharField(max_length=1000,blank=True,null=True)
    is_used = models.BooleanField(default=False, blank=False)
    state = models.BooleanField(default=False, blank=False)
    match_id = models.CharField(max_length=10,blank=True,null=True)
    ticket_price = models.IntegerField(validators=[MaxValueValidator(1),MinValueValidator(10000000)])
    

    def __str__(self):
        return f"Ticket for {self.user} to {self.place} on {self.buy_date}"
