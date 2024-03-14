from rest_framework import serializers
from .models import FoodModel, FoodCategory

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
        fields = ['title']