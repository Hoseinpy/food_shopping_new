from django.urls import path
from .views import LoginApiView, SingupApiView, LogoutApiView, ProfileApiView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login-api'),
    path('singup/', SingupApiView.as_view(), name='singup-api'),
    path('logout/', LogoutApiView.as_view(), name='logout-api'),
    path('profile/<code>', ProfileApiView.as_view(), name='profile-api'),
]
