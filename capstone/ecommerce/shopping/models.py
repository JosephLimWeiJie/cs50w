from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(
        max_length=100, blank=False, null=False, default="")
    gender = models.CharField(
        max_length=20, blank=False, null=False, default="Male")
    phone_number = models.IntegerField(
        blank=True, null=False, default=99887766)
    date_of_birth = models.DateField(
        blank=False, null=False, default="2000-12-30")

    def __str__(self):
        return self.full_name
