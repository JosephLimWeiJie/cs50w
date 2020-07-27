from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid


def index(request):
    listings = Listing.objects.all().filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_view(request):
    if request.method == "POST":
        title = request.POST['title']
        desrc = request.POST['desrc']
        bid_amount = request.POST['bid-amount']
        image_url = request.POST['image-url']
        category = request.POST['category']
        user = request.user

        listing = Listing.objects.create(
            title=title, desrc=desrc, image_url=image_url,
            category=category, user=user)
        new_bid = Bid.objects.create(
            listing=listing, amount=bid_amount, user=user)

        listing.save()
        new_bid.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")


@login_required
def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    curr_highest_bid = get_curr_highest_bid(listing)
    is_current_bid = check_current_bid(request, listing, curr_highest_bid)

    if request.method == "POST":
        new_bid = float(request.POST['new-bid'])
        # Error if new bid is lower than current bid
        if new_bid < curr_highest_bid:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "total_bid_count": listing.bid.all().count(),
                "curr_highest_bid": curr_highest_bid,
                "is_current_bid": is_current_bid,
                "error_message":
                    "You must enter a higher bid than the current bid."
            })
        else:
            # Update bid if higher than current bid
            new_bid = Bid.objects.create(
                listing=listing, amount=new_bid, user=request.user)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "total_bid_count": listing.bid.all().count(),
                "curr_highest_bid": format_curr_highest_bid(
                    get_curr_highest_bid(listing)),
                "is_current_bid": is_current_bid
            })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "curr_highest_bid": format_curr_highest_bid(curr_highest_bid),
            "is_current_bid": is_current_bid,
            "total_bid_count": listing.bid.all().count()
        })


def close_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    curr_highest_bid = get_curr_highest_bid(listing)
    listing.is_active = False
    listing.save()

    return render(request, "auctions/close.html", {
        "listing": listing,
        "curr_highest_bid": format_curr_highest_bid(curr_highest_bid),
        "total_bid_count": listing.bid.all().count(),
        "is_winner": is_winner(request, listing)
    })


""" Utility Functions """


def get_curr_highest_bid(listing):
    all_bids = listing.bid.all()
    curr_highest_bid = 0
    for bid in all_bids:
        if bid.amount > curr_highest_bid:
            curr_highest_bid = bid.amount
    return curr_highest_bid


def format_curr_highest_bid(curr_highest_bid):
    return "%s %0.2f" % ("$", curr_highest_bid)


def check_current_bid(request, listing, curr_highest_bid):
    """
    Returns True if the current user is the one with the
    highest bid currently.
    """
    if listing.user == request.user:
        if listing.bid == curr_highest_bid:
            return False
    return True


def is_winner(request, listing):
    """
    Returns True if the current user has won the auction and
    False if otherwise
    """
    if listing.user == request.user:
        return True
    return False
