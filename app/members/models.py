import os

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from config.settings.base import STATIC_DIR


class User(AbstractUser):
    blank_image_path = os.path.join(STATIC_DIR, 'static')

    img_profile = models.ImageField(
        upload_to='user',
        default=blank_image_path
    )

    nickname = models.CharField(max_length=16)

    def __str__(self):
        return self.username
