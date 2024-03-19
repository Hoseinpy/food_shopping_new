from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import UserModel
from .serializers import( LoginSerializer, SingupSerializer, ProfileSerializer,
ChangePasswordSerializer, CustomProfileSerializer, RestPasswordSerializer)
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .permissions import IsOwnerOrReadonly


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
            secret = serializer.data.get('secret')
            answer = serializer.data.get('answer')
            user = UserModel.objects.create(username=username, secret=secret, answer=answer)
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'status': 'singup successful'}, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        

# create logout api and set limit 5 request every minute
@method_decorator(ratelimit(key='ip', rate='5/m'), name='dispatch')
class LogoutApiView(APIView):
    def get(self, request):
        logout(request)
        return Response({'status': 'logout successful'}, status.HTTP_200_OK)
    

class ProfileApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = UserModel.objects.filter(id=request.user.id).first()
            serializer = ProfileSerializer(current_user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'you are not login'}, status.HTTP_401_UNAUTHORIZED)


# create change password api and set limit 4 request every minute
@method_decorator(ratelimit(key='ip', rate='4/m'), name='dispatch')
class ChangePassword(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user: UserModel = UserModel.objects.filter(id=request.user.id).first()
                if user.check_password(serializer.data.get('current_password')):
                    user.set_password(serializer.data.get('password'))
                    user.save()
                    logout(request) # new
                    return Response({'status': 'successful'}, status.HTTP_200_OK)
                else:
                    return Response({'status': 'current_password is worng'}, status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'you are not login'}, status.HTTP_401_UNAUTHORIZED)


class CustomProfileApiView(APIView):  # TODO: test full this api
    permission_classes = [IsOwnerOrReadonly]

    def put(self, request):
        if request.user.is_authenticated:
            user = UserModel.objects.filter(id=request.user.id).first()
            serializer = CustomProfileSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'successful'}, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'you are not login'}, status.HTTP_401_UNAUTHORIZED)



@method_decorator(ratelimit(key='ip', rate='5/m'), name='dispatch')
class RestPassword(APIView):
    def post(self, request):
        serializer = RestPasswordSerializer(data=request.data)
        if serializer.is_valid():
            secret = serializer.data.get('secret')
            answer = serializer.data.get('answer')
            user = UserModel.objects.filter(secret=secret, answer=answer).first()
            if user:
                password = serializer.data.get('password')
                user.set_password(password)
                user.save()
                return Response({'status': 'rest password is successful'}, status.HTTP_200_OK)
            else:
                return Response({'status': 'secret or answer is not currect'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)