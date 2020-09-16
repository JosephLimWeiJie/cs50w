from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class User(AbstractUser):
    order_total_price = models.FloatField(null=True, blank=True)
    has_new_notification = models.BooleanField(default=False)

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
    delivery_address = models.CharField(
        max_length=200, blank=True, null=True)

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
    price = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    listing_main_pic = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing", default=1)
    rating_score = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    quantity_sold = models.IntegerField(default=0)
    click_rate = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "desrc": self.desrc,
            "date": self.date,
            "quantity": self.quantity,
            "price": self.price,
            "listing_main_pic": self.listing_main_pic,
            "user": self.user,
            "rating_score": self.rating_score,
            "quantity_sold": self.quantity_sold,
            "click_rate": self.click_rate
        }


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="images", default=1)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.image}"


class Order(models.Model):
    STATUS = (
        ("To Ship", "To Ship"),
        ("To Receive", "To Receive"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Return/Refund", "Return/Refund"),
        ("Return Rejected", "Return Rejected"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order",
        null=True, blank=True)
    quantity_demanded = models.IntegerField(default=0)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="order",
        null=True, blank=True)
    status = models.CharField(
        max_length=64, default="To Ship", choices=STATUS)
    has_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s Order: {self.listing}"

    def serialize(self):
        return {
            "id": self.id,
            "quantity_demanded": self.quantity_demanded,
            "status": self.status
        }


class Review(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="review", default=1)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review", default=1)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="review", default=1)
    review = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.user}: {self.listing}"


class Notification(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="notification",
        null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="notification",
        null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification",
        null=True, blank=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="notification",
        null=True, blank=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="notification",
        null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    has_read = models.BooleanField(default=False)
    has_action = models.BooleanField(default=False)
    content = models.TextField()

    def __str__(self):
        return f"{self.user}'s Notification"
