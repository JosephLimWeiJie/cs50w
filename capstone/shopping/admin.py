from django.contrib import admin
from .models import User, Profile, Listing, ListingImage, Review, Order
from .models import Notification

# Register your models here.


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Notification)
