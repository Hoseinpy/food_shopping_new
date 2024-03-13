from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import UserModel
from .serializers import LoginSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


@method_decorator(ratelimit(key='ip', rate='5/m'), name='dispatch')
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
