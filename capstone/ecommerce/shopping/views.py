from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

from django import forms

from .models import User, Profile, Listing, ListingImage
from .forms import SignUpForm
import json

# Create your views here.


def index(request):
    return render(request, "shopping/index.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        full_name = request.POST["full_name"]
        gender = request.POST["gender"]
        phone_number = request.POST["phone_number"]
        date_of_birth = request.POST["date_of_birth"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "shopping/signup.html", {
                "message_password": "Passwords must match."
            })

        # Attempt to create new user and his/her profile
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            profile = Profile.objects.create(
                user=user, full_name=full_name, gender=gender,
                phone_number=phone_number,
                date_of_birth=parse_birthdate(date_of_birth))
            profile.save()
        except IntegrityError:
            return render(request, "shopping/signup.html", {
                "message_username": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shopping/signup.html", {
            "form": SignUpForm()
        })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "shopping/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "shopping/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile_view(request, name):
    profile = Profile.objects.get(user=request.user)
    listing_list = Listing.objects.all().filter(user=request.user)
    paginator = Paginator(listing_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "shopping/profile.html", {
        "name": name,
        "profile": profile,
        "hexed_phone_number": hex_phone_number(profile.phone_number),
        "hasListings": has_listings(request.user),
        "page_obj": page_obj
    })


@csrf_exempt
@login_required
def update_profile(request, profile_id):

    # Query for requested profile
    try:
        profile = Profile.objects.get(pk=profile_id)
    except profile.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return profile contents
    if request.method == "GET":
        return JsonResponse(profile.serialize())

    # Update profile content
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("email") is not None:
            request.user.email = data["email"]
        if data.get("gender") is not None:
            profile.gender = data["gender"]
        if data.get("phone_number") is not None:
            profile.phone_number = data["phone_number"]
        if data.get("date_of_birth") is not None:
            profile.date_of_birth = data["date_of_birth"]
        profile.save()
        request.user.save()
        return HttpResponse(status=204)

    # Profile must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def update_profile_pic(request):
    if request.method == 'POST':
        profile_to_update = Profile.objects.get(user=request.user)
        profile_to_update.profile_pic = request.FILES['myfile']
        profile_to_update.save()

        return render(request, "shopping/profile.html", {
            "name": request.user.username,
            "profile": profile_to_update,
            "hexed_phone_number": hex_phone_number(
                profile_to_update.phone_number)
        })


def create_listing_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        title = request.POST['title']
        desrc = request.POST['desrc']
        category = request.POST['category']
        quantity = request.POST['quantity']
        price = request.POST['price']
        listing = Listing.objects.create(
            title=title, desrc=desrc, category=category, quantity=quantity,
            price=price, user=request.user)

        images = request.FILES.getlist('image_files')

        count = 0
        for image in images:
            listing_image = ListingImage.objects.create(
                listing=listing, image=image)
            listing_image.save()

            if count == 0:
                listing.listing_main_pic = image
                count += 1

        listing.save()

        return render(request, "shopping/profile.html", {
            "name": request.user.username,
            "profile": profile,
            "hexed_phone_number": hex_phone_number(
                profile.phone_number)
        })
    else:
        return render(request, "shopping/profile.html", {
            "name": request.user.username,
            "profile": profile,
            "hexed_phone_number": hex_phone_number(
                profile.phone_number)
        })


def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing_images = ListingImage.objects.all().filter(listing=listing)
    listing_images_count = listing_images.count()
    return render(request, "shopping/listing.html", {
        "listing": listing,
        "listing_images": listing_images,
        "listing_images_count": listing_images_count
    })


""" Utility Functions """


def parse_birthdate(received_date_of_birth_repr):
    date_params = received_date_of_birth_repr.split("/")
    parsed_date_of_birth = (
        date_params[2] + "-" + date_params[0] + "-" + date_params[1])

    parsed_date_of_birth = datetime.strptime(parsed_date_of_birth, '%Y-%m-%d')
    return parsed_date_of_birth.date()


def hex_phone_number(number):
    phone_number_string = str(number)
    phone_number_length = len(phone_number_string)
    hexed_phone_number = ""

    for i in range(0, phone_number_length - 2):
        hexed_phone_number += "*"

    hexed_phone_number += (
        phone_number_string[phone_number_length - 2]
        + phone_number_string[phone_number_length - 1])

    return hexed_phone_number


def has_listings(user):
    if user.listing.all().count() != 0:
        return True
    return False
