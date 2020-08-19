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
import json
from django import forms

from .models import User, Profile

# Create your views here.


class SignUpForm(forms.Form):
    GENDER = [
     ('M', 'Male'),
     ('F', 'Female')
    ]

    full_name = forms.CharField(label="Full Name")
    password = forms.CharField(label="Password")
    gender = forms.ChoiceField(label="Gender", choices=GENDER)
    phone_number = forms.IntegerField(label="Phone Number")
    email = forms.EmailField(label="Email")

    birthday = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker4'
        })
    )


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
                phone_number=phone_number, date_of_birth=parse_birthdate(
                date_of_birth))
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
    return render(request, "shopping/profile.html", {
        "name": name
    })


""" Utility Functions """


def parse_birthdate(received_date_of_birth_repr):
    date_params = received_date_of_birth_repr.split("/")
    parsed_date_of_birth = (
        date_params[2] + "-" + date_params[0] + "-" + date_params[1])

    parsed_date_of_birth = datetime.strptime(parsed_date_of_birth, '%Y-%m-%d')
    return parsed_date_of_birth.date()
