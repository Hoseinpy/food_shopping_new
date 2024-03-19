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
    secret = serializers.CharField(max_length=50) # new
    answer = serializers.CharField(max_length=50) # new

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'error': 'password is not match'})
        
        elif UserModel.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'error': 'username is already take'})
        
        return attrs
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['avatar', 'username', 'first_name', 'last_name', 'bio']


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'error': 'password is not match'})

        return attrs


class CustomProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['avatar', 'username', 'first_name', 'last_name', 'bio']

    def validate(self, attrs):
        if UserModel.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'error': 'username is already take'})

        return attrs
    
# TODO:check this
class RestPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)
    secret = serializers.CharField(max_length=50)
    answer = serializers.CharField(max_length=50)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'error': 'password is not match'})

        return attrs
    
