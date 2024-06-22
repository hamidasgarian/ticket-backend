from rest_framework import serializers
from .models import *
from django.core.files import File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'email', 'national_id', 
                  'first_name', 'last_name', 'birthday', 'role')
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


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
        exclude = ['logo_filename']
        # fields = '__all__'

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
    
class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacity
        fields = '__all__'

def capacity(data):
    serializer = CapacitySerializer(data=data)

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

