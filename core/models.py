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
    password = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=11, blank=False, validators=[MinLengthValidator(11)],unique=True)
    national_id = models.CharField(max_length=10, blank=False, validators=[MinLengthValidator(10),only_digits_validator],unique=True)
    birthday = models.DateField(null=True, blank=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.national_id}"
        # return f"firstname is {self.first_name} and last name is {self.last_name}"

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
    buy_date = models.DateField(auto_now=True, blank=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)
    qr_code_id = models.CharField(max_length=1000,blank=True,null=True)
    is_used = models.BooleanField(default=False, blank=False)
    ticket_id = models.CharField(max_length=70,blank=False,null=False)
    global_seat_uique_id = models.CharField(max_length=60)

    def __str__(self):
        return f"Ticket for {self.user} to {self.stadium_name} on {self.buy_date}"
