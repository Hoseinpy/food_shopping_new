from django.contrib import admin
from .models import FoodCategory, FoodModel

@admin.register(FoodModel)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'price', 'rating', 'is_active']
    list_filter = ['category', 'rating', 'is_active']



@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url_title']
    list_filter = ['title']