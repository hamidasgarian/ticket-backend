from django.db import models
from django.core import validators
from django.core.validators import MinLengthValidator,MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def generate_logo_filename(team_name):
    return f"{team_name.replace(' ', '_').lower()}_logo.png"

def only_digits_validator(value):
    if not value.isdigit():
        raise ValidationError('This field should contain only digits.')

class Role(models.Model):
    name = models.CharField(max_length=50)

    def str(self):
        return self.name

class User(AbstractUser):
    phone_number = models.CharField(max_length=11,validators=[MinLengthValidator(11)],unique=True)
    national_id = models.CharField(max_length=10,validators=[MinLengthValidator(10),only_digits_validator],unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)   
    birthday = models.DateField(null=True, blank=True) 
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}:{self.phone_number}"
    

class Stadium(models.Model):
    stadium_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.stadium_name
    
class Match(models.Model):
    match_name = models.CharField(max_length=50, blank=False)
    match_id = models.CharField(max_length=10,blank=True,null=True)
    match_date = models.DateTimeField(null=True, blank=False)
    match_time = models.TimeField(null=True, blank=False)
    match_price = models.IntegerField(validators=[MaxValueValidator(10000000),MinValueValidator(1)])
    
    def __str__(self):
        return self.match_id

class Team(models.Model):
    team_name = models.CharField(max_length=50, blank=False)
    logo_filename = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.logo_filename:
            self.logo_filename = generate_logo_filename(self.team_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, db_column='match')
    host_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='host_team', db_column='host_team')
    guest_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='guest_team', db_column='guest_team')
    stadium_name = models.ForeignKey(Stadium, on_delete=models.CASCADE, db_column='stadium_name')
    stadium_row = models.CharField(max_length=10,blank=False,null=False)
    stadium_position = models.CharField(max_length=10,blank=False,null=False)
    stadium_seat =  models.CharField(max_length=10,blank=False,null=False)
    buy_date = models.DateTimeField(auto_now=True, blank=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)
    qr_code_id = models.CharField(max_length=1000,blank=True,null=True)
    is_used = models.BooleanField(default=False, blank=False)
    ticket_id = models.CharField(max_length=70,blank=False,null=False)
    global_seat_uique_id = models.CharField(max_length=60)

    def __str__(self):
        return f"Ticket for {self.user} to {self.stadium_name} on {self.buy_date}"
