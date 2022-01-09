from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True,
                              max_length=256)
    age = models.PositiveIntegerField(default=18)
