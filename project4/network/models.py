from django.contrib.auth.models import AbstractUser
from django.views.generic import ListView
from django.db import models
from datetime import datetime


class User(AbstractUser):
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    following = models.TextField(blank=True, null=True)

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "follower_count": self.follower_count,
            "following_count": self.following_count
        }


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post", default=1)
    content = models.TextField()
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "datetime": self.datetime
        }


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="like", default=0)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.like_count}"


class Follower(models.Model):
    name = models.CharField(max_length=64)
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower", blank=True)

    def __str__(self):
        return f"{self.name}"


class PostList(ListView):
    paginate_by = 10
    model = Post
