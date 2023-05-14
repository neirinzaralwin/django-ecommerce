from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = None

    # we want to login with email and password
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []