import os

from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.db import models
from reward.models import Reward


# Create your models here.
from config.settings.base import STATIC_DIR


class UserManager(DjangoUserManager):
    pass


class User(AbstractUser):
    blank_image_path = os.path.join(STATIC_DIR, 'static')
    print(blank_image_path)
    img_profile = models.ImageField(
        upload_to='user',
        default=blank_image_path
    )

    nickname = models.CharField(max_length=16)

    # funding = models.ManyToManyField(
    #     'self',
    #     symmetrical=False,
    #     through='Funding',
    #     blank=True,
    #     related_name='funding_list',
    #     related_query_name='funding_list'
    # )

    def __str__(self):
        return self.username


class Funding(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )

    reward = models.ForeignKey(
        Reward,
        on_delete=models.CASCADE,
        related_name='rewards'
    )

    username = models.CharField(max_length=20)

    phone_regex = RegexValidator(regex='\d{11}',
                                 message="Phone number must be 11 numbers")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True)

    address1 = models.CharField(max_length=30)

    address2 = models.CharField(max_length=30)

    comment = models.TextField()

    requested_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=1)
    cancel_at = models.DateTimeField(auto_now=True)
