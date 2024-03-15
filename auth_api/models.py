from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='user/avatar')
    bio = models.CharField(max_length=500)
    code = models.CharField(max_length=80, null=True)