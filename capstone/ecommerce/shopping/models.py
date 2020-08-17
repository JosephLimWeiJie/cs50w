from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    gender = models.CharField()
    phone_number = models.IntegerField()
    email = models.CharField(max_length=100)
    birthday = models.DateField()
