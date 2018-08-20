import os

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from config.settings.base import STATIC_DIR


class User(AbstractUser):

    img_profile = models.ImageField(
        upload_to='user',
        default='user/blank_user.png'
    )

    nickname = models.CharField(max_length=16)

    def __str__(self):
        return self.username
