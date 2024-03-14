from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import UserModel
from .serializers import LoginSerializer, SingupSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


# create login api and set limit 10 request every minute.
@method_decorator(ratelimit(key='ip', rate='10/m'), name='dispatch')
class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            if user is not None:
                current_user = user
                login(request, current_user)
                return Response({'status': 'login successful'}, status.HTTP_200_OK)
            else:
                return Response({'status': 'incurrect username or password'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'bad request'}, status.HTTP_400_BAD_REQUEST)


# create singup api and set limit 10 request every minute.
@method_decorator(ratelimit(key='ip', rate='10/m'), name='dispatch')
class SingupApiView(APIView):
    def post(self, request):
        serializer = SingupSerializer(data=request.data)
        if serializer.is_valid():
            # get username value and save in database
            username = serializer.data.get('username')
            user = UserModel.objects.create(username=username)
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'singup successful'}, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class LogoutApiView(APIView):
    def get(self, request):
        logout(request)
        return Response({'status': 'logout successful'}, status.HTTP_200_OK)