from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY = (
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'))

    title = models.CharField(max_length=64)
    desrc = models.TextField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True, choices=CATEGORY)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing", default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid",
        default=1)
    amount = models.FloatField(null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid", default=1
    )

    def __str__(self):
        return "%s %0.2f" % ("$", self.amount)
