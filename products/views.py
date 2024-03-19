from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FoodModel, FoodCategory, CartModel
from .serializers import FoodSerializer, FoodCategorySerializer, FoodDetailsSerializer, FoodCategoryDetailsSerializer, CartSerializer
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils.total_price import total_price
import requests
import json
from testmeshe.config_setting import MERCHANT, SANDBOX

class FoodApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            food = FoodModel.objects.filter(is_active=True)
            serializer = FoodSerializer(food, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


class FoodDetailsApiView(APIView):
    def get(self, request, food_id):
        if request.user.is_authenticated:
            food = FoodModel.objects.filter(is_active=True, id=food_id).first()
            serializer = FoodDetailsSerializer(food)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


# this api show all category food in database
class FoodCategoryApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            category = FoodCategory.objects.filter(is_active=True)
            serializer = FoodCategorySerializer(category, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status.HTTP_401_UNAUTHORIZED)


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
class CartDetailsApiView(APIView):

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
class CartAddApiView(APIView):

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
     


# sandbox merchant 
if SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

# zarinpal api
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


amount = 10000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/payment/verify/'


def send_request(request):
    data = {
        "MerchantID": MERCHANT,
        "Amount": amount,
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    
    data = json.dumps(data)
    
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(authority):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response