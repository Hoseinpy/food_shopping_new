from django.urls import path
from .views import LoginApiView, SingupApiView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login-api'),
    path('singup/', SingupApiView.as_view(), name='singup-api'),
]
