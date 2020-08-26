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


class Listing(models.Model):
    CATEGORY = (
        ("Men's Wear", "Men's Wear"),
        ("Women's Apparel", "Women's Apparel"),
        ("Mobile & Gadgets", "Mobile & Gadgets"),
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
    category = models.CharField(max_length=64, blank=True, choices=CATEGORY)
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing", default=1)


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="images", default=1)
    image = models.ImageField(null=True, blank=True)
