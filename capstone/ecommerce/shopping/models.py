from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }


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
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth
        }
