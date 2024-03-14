from django.urls import path
from .views import FoodApiView, FoodCategoryApiView, FoodDetailsApiView

urlpatterns = [
    path('v1/food/', FoodApiView.as_view(), name='food-list-api'),
    path('v1/food/<int:food_id>', FoodDetailsApiView.as_view(), name='food-details-api'),
    path('v1/category/', FoodCategoryApiView.as_view(), name='food-category-list-api'),
]


