from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post", default=1)
    content = models.TextField()
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.content}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="like", default=0)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.like_count}"


class Follower(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower", blank=True)
