from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='user/avatar', blank=True)
    bio = models.CharField(max_length=500, blank=True)
    secret = models.CharField(max_length=50, null=True)
    answer = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username