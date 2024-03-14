from django.urls import path
from .views import FoodApiView, FoodCategoryApiView, FoodDetailsApiView, FoodCategoryDetailsApiView

urlpatterns = [
    path('v1/food/', FoodApiView.as_view(), name='food-list-api'),
    path('v1/food/<int:food_id>', FoodDetailsApiView.as_view(), name='food-details-api'),
    path('v1/category/', FoodCategoryApiView.as_view(), name='food-category-list-api'),
    path('v1/category/<int:cat_id>', FoodCategoryDetailsApiView.as_view(), name='food-category-details-list-api'),
]


