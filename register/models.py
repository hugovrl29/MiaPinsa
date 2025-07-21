from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class Client(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    adresse = models.TextField(max_length=1000)
    phone = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
