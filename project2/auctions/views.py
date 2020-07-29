from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment

category_dict = {
    "menswear": "Men's Wear",
    "womenapparel": "Women's Apparel",
    "mobile": "Mobile & Gadgets",
    "beauty": "Beauty & Personal Care",
    "homeappliance": "Home Appliances",
    "homeliving": "Home & Living",
    "kidsfashion": "Kids Fashion",
    "toyskids": "Toys, Kids & Babies",
    "games": "Video Games",
    "food": "Food & Beverages",
    "computer": "Computer & Peripherals",
    "hobbies": "Hobbies & Books",
    "health": "Health & Wellness",
    "womensbags": "Women's Bags",
    "travel": "Travel & Luggage",
    "pet": "Pet Food & Supplies",
    "watches": "Watches",
    "jewel": "Jewellery & Accessory",
    "menshoes": "Men's Shoes",
    "womenshoes": "Women's Shoes",
    "sport": "Sports & Outdoors",
    "automotive": "Automotive",
    "menbags": "Men's Bags",
    "camera": "Cameras & Drones",
    "dining": "Dining, Travel & Services",
    "misc": "Miscellaneous"
}


def index(request):
    listings = Listing.objects.all().filter(is_active=True)
    curr_highest_bids = get_curr_highest_bid_for_each_listing(listings)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "curr_highest_bids": curr_highest_bids,
        "num_item_in_watchlist": get_watchlist_counter(request)
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


@login_required
def create_view(request):
    if request.method == "POST":
        title = request.POST['title']
        desrc = request.POST['desrc']
        bid_amount = request.POST['bid-amount']
        image_url = request.POST['image-url']
        category = request.POST['category']
        user = request.user

        try:
            # If image_url is not provided, use a placeholder image instead.
            if image_url is not None:
                image_url = "https://user-images.githubusercontent.com/"
                + "59989652/88834961-2aa0b280-d207-11ea-9e3d-24c488a75569.jpg"

            bid_amount = float(bid_amount)
            listing = Listing.objects.create(
                title=title, desrc=desrc, image_url=image_url,
                category=category, user=user)
            new_bid = Bid.objects.create(
                listing=listing, amount=bid_amount, user=user)

            listing.save()
            new_bid.save()
            return HttpResponseRedirect(reverse("index"))
        except (TypeError, ValueError):
            return render(request, "auctions/create.html", {
                "error_message": "Please enter a valid number for your bid."
            })
    else:
        return render(request, "auctions/create.html", {
            "num_item_in_watchlist": get_watchlist_counter(request)
        })


def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    curr_highest_bid = get_curr_highest_bid(listing)
    is_current_bid = check_current_bid(request, listing, curr_highest_bid)

    if request.method == "POST":
        new_bid = request.POST['new-bid']
        try:
            new_bid = float(new_bid)
        except (TypeError, ValueError):
            return render(request, "auctions/listing.html", {
                "is_on_watchlist": listing.is_on_watchlist,
                "listing": listing,
                "total_bid_count": listing.bid.all().count(),
                "curr_highest_bid": format_curr_highest_bid(curr_highest_bid),
                "is_current_bid": is_current_bid,
                "error_message":
                    "You must enter a valid number for your new bid.",
                "comments": listing.comment.all(),
                "num_item_in_watchlist": get_watchlist_counter(request)
            })
        # Error if new bid is lower than current bid
        if new_bid < curr_highest_bid:
            return render(request, "auctions/listing.html", {
                "is_on_watchlist": listing.is_on_watchlist,
                "listing": listing,
                "total_bid_count": listing.bid.all().count(),
                "curr_highest_bid": format_curr_highest_bid(curr_highest_bid),
                "is_current_bid": is_current_bid,
                "error_message":
                    "You must enter a higher bid than the current bid.",
                "comments": listing.comment.all(),
                "num_item_in_watchlist": get_watchlist_counter(request)
            })
        else:
            # Update bid if higher than current bid
            new_bid = Bid.objects.create(
                listing=listing, amount=new_bid, user=request.user)
            return render(request, "auctions/listing.html", {
                "is_on_watchlist": listing.is_on_watchlist,
                "listing": listing,
                "total_bid_count": listing.bid.all().count(),
                "curr_highest_bid": format_curr_highest_bid(
                    get_curr_highest_bid(listing)),
                "is_current_bid": is_current_bid,
                "comments": listing.comment.all(),
                "num_item_in_watchlist": get_watchlist_counter(request)
            })
    else:
        return render(request, "auctions/listing.html", {
            "is_on_watchlist": listing.is_on_watchlist,
            "listing": listing,
            "curr_highest_bid": format_curr_highest_bid(curr_highest_bid),
            "is_current_bid": is_current_bid,
            "total_bid_count": listing.bid.all().count(),
            "comments": listing.comment.all(),
            "num_item_in_watchlist": get_watchlist_counter(request)
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
        "is_winner": is_winner(request, listing),
        "num_item_in_watchlist": get_watchlist_counter(request)
    })


def add_comment_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        comment = request.POST['comment']
        new_comment = Comment.objects.create(
            listing=listing, user=request.user, comment=comment)

        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        return render(request, "auctions/comment.html", {
            "listing": listing,
            "num_item_in_watchlist": get_watchlist_counter(request)
        })


@login_required
def watchlist(request):
    watchlist = Listing.objects.all().filter(
        is_on_watchlist=True, is_active=True)

    curr_highest_bids = get_curr_highest_bid_for_each_listing(watchlist)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "curr_highest_bids": curr_highest_bids,
        "num_item_in_watchlist": get_watchlist_counter(request)
    })


def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.is_on_watchlist = True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.is_on_watchlist = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def category(request):
    return render(request, "auctions/category.html", {
        "num_item_in_watchlist": get_watchlist_counter(request)
    })


def category_listing(request, category_name):
    category_value = category_dict[category_name]
    relevant_listings = Listing.objects.all().filter(
        category=category_value, is_active=True)
    curr_highest_bids = get_curr_highest_bid_for_each_listing(
        relevant_listings)

    return render(request, "auctions/categorylisting.html", {
        "relevant_listings": relevant_listings,
        "curr_highest_bids": curr_highest_bids,
        "num_item_in_watchlist": get_watchlist_counter(request)
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


def get_curr_highest_bid_for_each_listing(listings):
    """
    Returns a dictionary storing highest bid for each listing.
    """
    curr_highest_bids = {}
    for listing in listings:
        if listing not in curr_highest_bids:
            curr_highest_bids[listing] = format_curr_highest_bid(
                get_curr_highest_bid(listing))
        else:
            curr_highest_bids[listing] = format_curr_highest_bid(
                get_curr_highest_bid(listing))
    return curr_highest_bids


def get_watchlist_counter(request):
    num_item_in_watchlist = None

    if request.user.is_authenticated:
        num_item_in_watchlist = Listing.objects.all().filter(
            is_on_watchlist=True, is_active=True).count()

    return num_item_in_watchlist
