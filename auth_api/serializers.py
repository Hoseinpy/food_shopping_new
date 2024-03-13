from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=50)
    

class SingupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'error': 'the pasword is not match'})
        
        elif UserModel.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'error': 'the username is already take'})
        
        return attrs
    
    