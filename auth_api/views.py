from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import UserModel
from .serializers import LoginSerializer, SingupSerializer, ProfileSerializer, ChangePasswordSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from django.utils.crypto import get_random_string


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
                UserModel.objects.filter(id=user.id).update(code=get_random_string(72))
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
            user = UserModel.objects.create(username=username, code=get_random_string(72))
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'singup successful'}, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        

# create logout api and set limit 1 request every minute
@method_decorator(ratelimit(key='ip', rate='2/m'), name='dispatch')
class LogoutApiView(APIView):
    def get(self, request):
        logout(request)
        return Response({'status': 'logout successful'}, status.HTTP_200_OK)
    

# create profile api and set limit 20 request every minute
@method_decorator(ratelimit(key='ip', rate='20/m'), name='dispatch')
class ProfileApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = UserModel.objects.filter(id=request.user.id).first()
            serializer = ProfileSerializer(current_user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'you are not login'}, status.HTTP_401_UNAUTHORIZED)


class ChangePassword(APIView):
    def post(self, request):
        pass
        # serializer = ChangePasswordSerializer(data=request.data)
        # if serializer.is_valid():
        #     user: UserModel = get_object_or_404(UserModel, code=code)
        #     if user.check_password(serializer.data.get('current_password')):
        #         user.set_password(serializer.data.get('password'))
        #         user.save()
                  #return Response({'status': 'successful'}, status.HTTP_200_OK)
        #     else:
        #         return Response({'status': 'incorrect current password'}, status.HTTP_404_NOT_FOUND)
        # else:
        #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)