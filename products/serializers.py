from rest_framework import serializers
from .models import FoodModel, FoodCategory, CartModel

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodModel
        fields = ['id', 'image', 'name', 'rating', 'short_description']


class FoodDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodModel
        fields = '__all__'


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['image', 'title']


class FoodCategoryDetailsSerializer(serializers.ModelSerializer):
    category_food = FoodSerializer(read_only=True, many=True)
    class Meta:
        model = FoodCategory
        fields = ['title', 'category_food']


class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1)
    food = serializers.SerializerMethodField()

    class Meta:
        model = CartModel
        fields = ['id', 'food', 'quantity', 'finall_price', 'created_at']

    def get_food(self, obj):
        return str(obj.food)


