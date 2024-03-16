from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FoodModel, FoodCategory, CartModel
from .serializers import FoodSerializer, FoodCategorySerializer, FoodDetailsSerializer, FoodCategoryDetailsSerializer, CartSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# this api show all food in database.
@method_decorator([ratelimit(key='ip', rate='500/m'), csrf_exempt], name='dispatch')
class FoodApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            food = FoodModel.objects.filter(is_active=True)
            serializer = FoodSerializer(food, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


# this api show food details
@method_decorator(ratelimit(key='ip', rate='100/m'), name='dispatch')
class FoodDetailsApiView(APIView):
    def get(self, request, food_id):
        if request.user.is_authenticated:
            food = FoodModel.objects.filter(is_active=True, id=food_id).first()
            serializer = FoodDetailsSerializer(food)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


# this api show all category food in database
@method_decorator(ratelimit(key='ip', rate='100/m'), name='dispatch')
class FoodCategoryApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            category = FoodCategory.objects.filter(is_active=True)
            serializer = FoodCategorySerializer(category, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


# this api show all food from one category
@method_decorator(ratelimit(key='ip', rate='100/m'), name='dispatch')
class FoodCategoryDetailsApiView(APIView):
    def get(self, request, cat_id):
        if request.user.is_authenticated:
            category = FoodCategory.objects.filter(is_active=True, id=cat_id).first()
            serializer = FoodCategoryDetailsSerializer(category)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)   


# this api show all user cart
class CartListApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            cart = CartModel.objects.filter(user=request.user).order_by('-created_at')
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


# this api show detail and can delete and update cart
@method_decorator([ratelimit(key='ip', rate='20/m'), csrf_exempt], name='dispatch')
class CartDetailsApiView(APIView):
    def get(self, request, cart_id):
        if request.user.is_authenticated:
            cart = get_object_or_404(CartModel, id=cart_id)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)

    def put(self, request, cart_id):
        if request.user.is_authenticated:
            cart = get_object_or_404(CartModel, id=cart_id)
            serializer = CartSerializer(instance=cart, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'cart is successfully update'}, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, cart_id):
        if request.user.is_authenticated:
            cart = get_object_or_404(CartModel, id=cart_id)
            if cart.user == request.user:
                cart.delete()
                return Response({'status': 'cart is successfully deleted'}, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


# this api for add food to cart
@method_decorator([ratelimit(key='ip', rate='10/m'), csrf_exempt], name='dispatch')
class CartAddApiView(APIView):
    def post(self, request, food_id):
        if request.user.is_authenticated:
            food = get_object_or_404(FoodModel, id=food_id)
            print(food)
            cart = CartModel.objects.filter(user=request.user, food=food).first()
            print(cart)

            if cart:
                cart.quantity += 1
                cart.save()
                return Response({'status': 'quantity is added'}, status.HTTP_200_OK)

            else:
                create_cart = CartModel.objects.create(user=request.user, food=food, quantity=request.data.get('quantity'))
                create_cart.save()
                return Response({'status': 'cart succecful created'}, status.HTTP_201_CREATED)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)

