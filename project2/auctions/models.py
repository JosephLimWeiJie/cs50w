from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY = (
        ("Men's Wear", "Men's Wear"),
        ("Women's Apparel", "Women's Apparel"),
        ("Mobile & Gadgets", "MMobile & Gadgets"),
        ("Beauty & Personal Care", "Beauty & Personal Care"),
        ("Home Appliances", "Home Appliances"),
        ("Home & Living", "Home & Living"),
        ("Kids Fashion", "Kids Fashion"),
        ("Toys, Kids & Babies", "Toys, Kids & Babies"),
        ("Video Games", "Video Games"),
        ("Food & Beverages", "Food & Beverages"),
        ("Computers & Peripherals", "Computers & Peripherals"),
        ("Hobbies & Books", "Hobbies & Books"),
        ("Health & Wellness", "Health & Wellness"),
        ("Women's Bags", "Women's Bags"),
        ("Travel & Luggage", "Travel & Luggage"),
        ("Pet Food & Supplies", "Pet Food & Supplies"),
        ("Watches", "Watches"),
        ("Jewellery & Accessory", "Jewellery & Accessory"),
        ("Men's Shoes", "Men's Shoes"),
        ("Women's Shoes", "Women's Shoes"),
        ("Sports & Outdoors", "Sports & Outdoors"),
        ("Automotive", "Automotive"),
        ("Men's Bags", "Men's Bags"),
        ("Cameras & Drones", "Cameras & Drones"),
        ("Dining, Travel & Services", "Dining, Travel & Services"),
        ("Miscellaneous", "Miscellaneous"))

    title = models.CharField(max_length=64)
    desrc = models.TextField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True, choices=CATEGORY)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing", default=1)
    is_active = models.BooleanField(default=True)
    is_on_watchlist = models.BooleanField(default=False)

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


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comment",
        default=None)
    comment = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment", default=None)

    def __str__(self):
        return f"{self.user}: {self.comment}"
