from rest_framework import serializers
from .models import *

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
