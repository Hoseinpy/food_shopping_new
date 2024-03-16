from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    avatar = models.ImageField(upload_to='user/avatar', blank=True)
    bio = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.username