from django.urls import path
from .views import LoginApiView, SingupApiView, LogoutApiView, ProfileApiView, ChangePassword

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login-api'),
    path('singup/', SingupApiView.as_view(), name='singup-api'),
    path('logout/', LogoutApiView.as_view(), name='logout-api'),
    path('profile/', ProfileApiView.as_view(), name='profile-api'),
    path('profile/change-password/', ChangePassword.as_view(), name='change-password-api'),
]
