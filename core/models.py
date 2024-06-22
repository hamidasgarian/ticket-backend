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
    
    

class Team(models.Model):
    team_name = models.CharField(max_length=50, blank=False)
    logo_filename = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.logo_filename:
            self.logo_filename = generate_logo_filename(self.team_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name
    
class Capacity(models.Model):
    total_positions = models.PositiveIntegerField(default=10)
    rows_per_position = models.PositiveIntegerField(default=10)
    seats_per_row = models.PositiveIntegerField(default=30)
    
    number_of_host_positions = models.PositiveIntegerField(default=7)
    number_of_guest_positions = models.PositiveIntegerField(default=3)
    
    all_available_seats = models.PositiveIntegerField(default=3000)
    all_available_host_seats = models.PositiveIntegerField(default=2100)
    all_available_guest_seats = models.PositiveIntegerField(default=900)
    
    available_seats_per_position_host = models.JSONField(default=list)
    available_seats_per_position_guest = models.JSONField(default=list)

    seat_costs_per_position = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.available_seats_per_position_host = [self.rows_per_position * self.seats_per_row] * self.number_of_host_positions
            self.available_seats_per_position_guest = [self.rows_per_position * self.seats_per_row] * self.number_of_guest_positions
        super().save(*args, **kwargs)

    def get_all_available_seats(self, match_id):
        capacity = Capacity.objects.get(id=match_id)
        return capacity.all_available_host_seats + capacity.all_available_guest_seats

    def available_seat_per_positions(self, match_id, position_number, seat_type):
        capacity = Capacity.objects.get(id=match_id)
        if seat_type == 'host':
            return capacity.available_seats_per_position_host[position_number]
        elif seat_type == 'guest':
            return capacity.available_seats_per_position_guest[position_number]
        else:
            raise ValueError("Invalid seat type.")

    def available_seat_per_rows(self, match_id, position_number, row_number, seat_type):
        capacity = Capacity.objects.get(id=match_id)
        if seat_type == 'host':
            if position_number >= len(capacity.available_seats_per_position_host):
                raise ValueError("Invalid position number for host.")
            return capacity.available_seats_per_position_host[position_number] // self.rows_per_position
        elif seat_type == 'guest':
            if position_number >= len(capacity.available_seats_per_position_guest):
                raise ValueError("Invalid position number for guest.")
            return capacity.available_seats_per_position_guest[position_number] // self.rows_per_position
        else:
            raise ValueError("Invalid seat type.")

    def sell_ticket(self, match_id, position_number, row_number, seat_type):
        capacity = Capacity.objects.get(id=match_id)
        position_number = int(position_number) - 1  
        row_number = int(row_number) - 1  
        
        if seat_type == 'host':
            if capacity.available_seats_per_position_host[position_number] > 0:
                capacity.available_seats_per_position_host[position_number] -= 1
                capacity.all_available_seats -= 1
                capacity.all_available_host_seats -= 1
                capacity.save()
            else:
                raise ValueError("No available host seats in this position.")
        elif seat_type == 'guest':
            if capacity.available_seats_per_position_guest[position_number] > 0:
                capacity.available_seats_per_position_guest[position_number] -= 1
                capacity.all_available_seats -= 1
                capacity.all_available_guest_seats -= 1
                capacity.save()
            else:
                raise ValueError("No available guest seats in this position.")
        else:
            raise ValueError("Invalid seat type.")
            
        
class Match(models.Model):
    match_name = models.CharField(max_length=50, blank=False)
    match_number = models.CharField(max_length=10,blank=True,null=True)
    match_date = models.DateField(null=True, blank=False)
    match_time = models.TimeField(null=True, blank=False)
    host_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='host_team', db_column='host_team')
    guest_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='guest_team', db_column='guest_team')
    capacity = models.ForeignKey(Capacity, on_delete=models.CASCADE, db_column='capacity')

    def __str__(self):
        return self.match_number
    
    


class Stadium(models.Model):
    stadium_name = models.CharField(max_length=50, blank=False)
    stadium_total_positions = models.JSONField(default=list)
    stadium_host_positions = models.JSONField(default=list)
    stadium_guest_positions = models.JSONField(default=list)
    stadium_rows_in_host_positions = models.JSONField(default=list)
    stadium_rows_in_guest_positions = models.JSONField(default=list)
    stadium_seats = models.JSONField(default=list)

    stadium_seat_category1 = models.JSONField(default=list)
    stadium_seat_category2 = models.JSONField(default=list)
    stadium_seat_category3 = models.JSONField(default=list)
    stadium_seat_category4 = models.JSONField(default=list)

    def __str__(self):
        return self.stadium_name
    
        
    
class Ticket(models.Model):
    mobile = models.CharField(max_length=11, null=True, blank=True)
    seat_owner = models.CharField(max_length=50, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, db_column='match')
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, db_column='capacity')
    seat_type = models.CharField(max_length=6, blank=False)
    seat_position = models.CharField(max_length=6, blank=False)
    seat_row = models.CharField(max_length=6, blank=False)
    seat_number = models.CharField(max_length=6, blank=False)
    buy_date = models.DateField(auto_now_add=True)
    # qr_code = models.ImageField(upload_to='qr_codes/', blank=True,null=True)
    # qr_code_id = models.CharField(max_length=100,blank=True,null=True)
    seat_availibility = models.BooleanField(default=True, blank=False)
    ticket_used = models.BooleanField(default=False, blank=False)
    ticket_id = models.CharField(max_length=70,blank=False,null=False)
    seat_costs = models.IntegerField()
    

    def __str__(self):
        return f"Ticket for {self.seat_owner} to {self.stadium_name} on {self.buy_date}"
    
    @classmethod
    def get_by_mobile(cls, mobile):
        return cls.objects.filter(mobile=mobile)
    
    @classmethod
    def get_unavailable_seats_by_match(cls, match_id):
        return cls.objects.filter(seat_availibility=False, match_id=match_id).values_list('seat_number', flat=True)


    


