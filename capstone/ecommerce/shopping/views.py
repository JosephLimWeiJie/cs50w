from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django import forms

# Create your views here.


class NewSignUpForm(forms.Form):
    GENDER = [
     ('M', 'Male'),
     ('F', 'Female')
    ]

    full_name = forms.CharField(label="Full Name")
    password = forms.CharField(label="Password")
    gender = forms.ChoiceField(label="Gender", choices=GENDER)
    phone_number = forms.IntegerField(label="Phone Number")
    email = forms.EmailField(label="Email")

    birthday = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


def index(request):
    return render(request, "shopping/index.html")


def signup(request):
    return render(request, "shopping/signup.html", {
        "form": NewSignUpForm()
    })
