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
from utils.total_price import total_price


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
    authentication_classes = [TokenAuthentication]

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
    authentication_classes = [TokenAuthentication]

    def get(self, request, cart_id):
        if request.user.is_authenticated:
            cart = CartModel.objects.filter(id=cart_id).first()
            if cart:
                serializer = CartSerializer(cart)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response({'status': 'not found'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)

    def put(self, request, cart_id):
        if request.user.is_authenticated:
            cart = get_object_or_404(CartModel, id=cart_id)
            serializer = CartSerializer(instance=cart, data=request.data)
            if serializer.is_valid():
                quantity = serializer.validated_data.get('quantity')
                if quantity > cart.quantity or quantity < cart.quantity:
                    p = quantity * cart.food.price
                    cart.finall_price = p
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
    authentication_classes = [TokenAuthentication]

    def post(self, request, food_id):
        if request.user.is_authenticated:
            food = get_object_or_404(FoodModel, id=food_id)
            cart = CartModel.objects.filter(user=request.user, food=food).first()

            if cart:
                return Response({'status': 'food is already added your cart'}, status.HTTP_302_FOUND)

            else:
                quantity = request.data.get('quantity')
                if quantity is None:
                    quantity = 1
                else:
                    quantity = request.data.get('quantity')
                p = total_price(quantity=quantity, price=food.price)
                create_cart = CartModel.objects.create(user=request.user, food=food, quantity=quantity, finall_price=p)
                create_cart.save()
                return Response({'status': 'cart succecful created'}, status.HTTP_201_CREATED)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)

