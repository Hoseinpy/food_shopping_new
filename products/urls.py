from django.urls import path
from .views import (
    FoodApiView, FoodCategoryApiView, FoodDetailsApiView, FoodCategoryDetailsApiView,
    CartListApiView, CartDetailsApiView, CartAddApiView,
)

urlpatterns = [
    path('v1/food/', FoodApiView.as_view(), name='food-list-api'),
    path('v1/food/<int:food_id>', FoodDetailsApiView.as_view(), name='food-details-api'),
    path('v1/category/', FoodCategoryApiView.as_view(), name='food-category-list-api'),
    path('v1/category/<int:cat_id>', FoodCategoryDetailsApiView.as_view(), name='food-category-details-list-api'),
    path('v1/cart/', CartListApiView.as_view(), name='cart-list-api'),
    path('v1/cart/<int:cart_id>', CartDetailsApiView.as_view(), name='cart-detail-api'),
    path('v1/food/add/<int:food_id>', CartAddApiView.as_view(), name='cart-add-api'),
]


