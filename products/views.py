from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FoodModel, FoodCategory
from .serializers import FoodSerializer, FoodCategorySerializer, FoodDetailsSerializer, FoodCategoryDetailsSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


# create food api and set limit 500 request every minute
@method_decorator(ratelimit(key='ip', rate='500/m'), name='dispatch')
class FoodApiView(APIView):
    def get(self, request):
        food = FoodModel.objects.filter(is_active=True)
        serializer = FoodSerializer(food, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


# create food api and set limit 100 request every minute
@method_decorator(ratelimit(key='ip', rate='100/m'), name='dispatch')
class FoodDetailsApiView(APIView):
    def get(self, request, food_id):
        food = FoodModel.objects.filter(is_active=True, id=food_id).first()
        serializer = FoodDetailsSerializer(food)
        return Response(serializer.data, status.HTTP_200_OK)
    


# create food category api and set limit 100 request every minute
@method_decorator(ratelimit(key='ip', rate='100/m'), name='dispatch')
class FoodCategoryApiView(APIView):
    def get(self, request):
        category = FoodCategory.objects.filter(is_active=True)
        serializer = FoodCategorySerializer(category, many=True)
        return Response(serializer.data, status.HTTP_200_OK)



# create category detail api and set limit 100 request every minute
@method_decorator(ratelimit(key='ip', rate='100/m'), name='dispatch')
class FoodCategoryDetailsApiView(APIView):
    def get(self, request, cat_id):
        category = FoodCategory.objects.filter(is_active=True, id=cat_id).first()
        serializer = FoodCategoryDetailsSerializer(category)
        return Response(serializer.data, status.HTTP_200_OK)
