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

from .models import User, Profile, Listing, ListingImage, Review, Order
from .forms import SignUpForm
import json

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
    all_listing = Listing.objects.all()
    top_products = Listing.objects.all().order_by("quantity_sold")
    trending_searches = Listing.objects.all().order_by("click_rate").reverse()

    return render(request, "shopping/index.html", {
        "all_listing": all_listing,
        "top_products": top_products,
        "trending_searches": trending_searches,
    })


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
    listing_paginator = Paginator(listing_list, 10)
    listing_page_number = request.GET.get('page')
    listing_page_obj = listing_paginator.get_page(listing_page_number)

    review_list = Review.objects.all()
    review_paginator = Paginator(review_list, 10)
    review_page_number = request.GET.get('page')
    review_page_obj = review_paginator.get_page(review_page_number)

    order_list = Order.objects.all().filter(user=request.user)
    order_paginator = Paginator(order_list, 10)
    order_page_number = request.GET.get('page')
    order_page_obj = order_paginator.get_page(order_page_number)

    return render(request, "shopping/profile.html", {
        "name": name,
        "profile": profile,
        "hexed_phone_number": hex_phone_number(profile.phone_number),
        "hasListings": has_listings(request.user),
        "listing_page_obj": listing_page_obj,
        "review_page_obj": review_page_obj,
        "order_page_obj": order_page_obj,
        "hasPurchases": check_user_has_purchases(request.user, order_list),
        "hasReviews": check_user_has_reviewed(request.user, review_list),
        "hasItemSold": check_user_has_item_sold(request.user, order_list)
    })


@csrf_exempt
@login_required
def update_profile(request, profile_id):

    # Query for requested profile
    try:
        profile = Profile.objects.get(pk=profile_id)
    except profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)

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


def update_profile_delivery_addr(request):
    if request.method == 'POST':
        profile_to_update = Profile.objects.get(user=request.user)
        profile_to_update.delivery_address = request.POST['addr_text']
        profile_to_update.save()

        return render(request, "shopping/checkout.html", {
            "profile": profile_to_update
        })
    else:
        return render(request, "shopping/checkout.html", {
            "profile": profile_to_update
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
                profile.phone_number),
        })
    else:
        return render(request, "shopping/profile.html", {
            "name": request.user.username,
            "profile": profile,
            "hexed_phone_number": hex_phone_number(
                profile.phone_number),
        })


def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing_images = ListingImage.objects.all().filter(listing=listing)
    listing_images_count = listing_images.count()
    review_list = Review.objects.all()
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "shopping/listing.html", {
        "listing": listing,
        "listing_images": listing_images,
        "listing_images_count": listing_images_count,
        "hasReviews": check_listing_review(listing),
        "reviews": Review.objects.filter(listing=listing),
        "hasReviewed": check_user_has_reviewed(
            request.user, Review.objects.filter(listing=listing)),
        "page_obj": page_obj,
        "hasSoldOut": check_listing_has_sold_out(listing),
        "total_review_count": Review.objects.filter(listing=listing).count(),
        "listing_rating_score": parse_rating_score_one_decimal_place(
            listing.rating_score),
        "hasListingInCart": check_listing_exist_in_cart(listing, request.user)
    })


def update_listing_desrc_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing_images = ListingImage.objects.all().filter(listing=listing)
    listing_images_count = listing_images.count()

    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        quantity = request.POST['quantity']
        price = request.POST['price']
        edited_product_desrc = request.POST['edited_desrc_text']

        images = request.FILES.getlist('image_files')

        count = 0
        for image in images:
            listing_image = ListingImage.objects.create(
                listing=listing, image=image)
            listing_image.save()

            if count == 0:
                listing.listing_main_pic = image
                count += 1

        listing.title = title
        listing.category = category
        listing.quantity = quantity
        listing.price = price
        listing.desrc = edited_product_desrc
        listing.save()

        return render(request, "shopping/listing.html", {
            "listing": listing,
            "listing_images": listing_images,
            "listing_images_count": listing_images_count,
            "reviews": Review.objects.all(),
        })
    else:
        return render(request, "shopping/listing.html", {
            "listing": listing,
            "listing_images": listing_images,
            "listing_images_count": listing_images_count,
            "reviews": Review.objects.all(),
        })


def review_view(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        profile = Profile.objects.get(user=request.user)
        review = request.POST['review_text']
        rating = request.POST['rating-form-input']
        review = Review.objects.create(
            listing=listing, user=request.user, profile=profile,
            review=review, rating=rating)

        review.save()
        update_listing_rating_score(listing)
        return listing_view(request, listing_id)
    else:
        return listing_view(request, listing_id)


def update_review_view(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        review = Review.objects.get(user=request.user, listing=listing)
        review.review = request.POST['edited-review-text']
        review.rating = request.POST['edited-rating-form-input']
        review.save()
        update_listing_rating_score()
        return listing_view(request, listing_id)
    else:
        return listing_view(request, listing_id)


def category_view(request, category_name):
    category_value = category_dict[category_name]
    relevant_listings = Listing.objects.all().filter(category=category_value)
    return render(request, "shopping/category.html", {
        "category_name": category_name,
        "relevant_listings": relevant_listings
    })


def category_sort_view(request):
    if request.method == "GET":
        category_name = request.GET.get('category-name')
        category_value = category_dict[category_name]
        if 'popular-btn' in request.GET:
            sorted_popular_listings = Listing.objects.all().filter(
                category=category_value).order_by("rating_score").reverse()

            return render(request, "shopping/category.html", {
                "category_name": category_name,
                "relevant_listings": sorted_popular_listings
            })
        elif 'lastest-btn' in request.GET:
            sorted_latest_listings = Listing.objects.all().filter(
                category=category_value).order_by("date").reverse()

            return render(request, "shopping/category.html", {
                "category_name": category_name,
                "relevant_listings": sorted_latest_listings
            })
        elif 'price-btn' in request.GET:
            sorted_price_listings = Listing.objects.all().filter(
                category=category_value).order_by("price").reverse()

            return render(request, "shopping/category.html", {
                "category_name": category_name,
                "relevant_listings": sorted_price_listings
            })


@login_required
def cart_view(request):
    if request.method == 'POST':
        listing_id = request.POST['listing-id']
        listing = Listing.objects.get(id=listing_id)

        quantity_demanded = request.POST['quantity-demanded']
        order = Order.objects.create(
            user=request.user, listing=listing,
            quantity_demanded=quantity_demanded)

        order.save()
        total_order_price = parse_order_total_price_two_decimal_pace(
            get_total_price_in_cart(request.user))

        order_list = Order.objects.filter(user=request.user, has_purchased=False)
        paginator = Paginator(order_list, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        return render(request, "shopping/cart.html", {
            "orders": orders,
            "total_order_price": total_order_price,
            "hasOrderInCart": check_user_has_order_in_cart(request.user)
        })
    else:
        order_list = Order.objects.filter(user=request.user, has_purchased=False)
        paginator = Paginator(order_list, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        total_order_price = parse_order_total_price_two_decimal_pace(
            get_total_price_in_cart(request.user))
        return render(request, "shopping/cart.html", {
            "orders": orders,
            "total_order_price": total_order_price,
            "hasOrderInCart": check_user_has_order_in_cart(request.user)
        })


@login_required
def update_cart_view(request):
    if request.method == 'POST':
        listing_to_remove_id = request.POST['listing-to-remove']
        listing_to_remove = Listing.objects.get(id=listing_to_remove_id)
        order_to_remove = Order.objects.filter(listing=listing_to_remove)
        order_to_remove.delete()

        return render(request, "shopping/cart.html", {
            "orders": Order.objects.filter(user=request.user)
        })
    else:
        return render(request, "shopping/cart.html", {
            "orders": Order.objects.filter(user=request.user)
        })


@csrf_exempt
@login_required
def update_listing(request, listing_id):

    # Query for requested listing
    try:
        listing = Listing.objects.get(pk=listing_id)
    except listing.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)

    # Return listing contents
    if request.method == "GET":
        return JsonResponse(listing.serialize())

    # Update listing contents
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("click_rate") is not None:
            listing.click_rate = data["click_rate"]
        listing.save()
        request.user.save()
        return HttpResponse(status=204)

    # Listing must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def update_order(request, order_id):

    # Query for requested order
    try:
        order = Order.objects.get(pk=order_id)
    except order.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)

    # Return order contents
    if request.method == "GET":
        return JsonResponse(order.serialize())

    # Update order contents
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("quantity_demanded") is not None:
            order.quantity_demanded = data["quantity_demanded"]
        if data.get("status") is not None:
            order.status = data["status"]
        order.save()
        request.user.save()
        return HttpResponse(status=204)

    # Order must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def checkout_view(request):
    """
    Note that this method does not store any credit card
    information and will just redirect the user to 'Track
    my Order page'.
    """
    if request.method == 'POST':
        orders_in_cart = Order.objects.filter(user=request.user)
        update_listing_quantity(orders_in_cart)
        return HttpResponseRedirect(
            reverse("trackorder", args=[request.user]))
    else:
        order_list = Order.objects.filter(user=request.user)
        paginator = Paginator(order_list, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        return render(request, "shopping/checkout.html", {
            "profile": Profile.objects.get(user=request.user),
            "orders": orders
        })


def track_order_view(request, name):
    order_list = Order.objects.filter(user=request.user)
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    return render(request, "shopping/trackorder.html", {
        "profile": Profile.objects.get(user=request.user),
        "orders": orders,
        "hasOrders": check_user_has_order(request.user)
    })


def receive_order(request):
    if request.method == "POST":
        order_id = request.POST['order_id']
        order = Order.objects.get(pk=order_id)
        order.status = "Completed"
        order.save()
        return HttpResponseRedirect(
            reverse("trackorder", args=[request.user]))
    else:
        return HttpResponseRedirect(
            reverse("trackorder", args=[request.user]))


def search_view(request):
    if request.method == "POST":
        search_keywords = request.POST['search_keywords']
        relevant_listings = get_relevant_listings(search_keywords)
        relevant_users = get_relevant_users(search_keywords)
        relevant_categories = get_relevant_categories(relevant_listings)

        return render(request, "shopping/search.html", {
            "search_keywords": search_keywords,
            "relevant_listings": relevant_listings,
            "relevant_users": relevant_users,
            "relevant_categories": relevant_categories
        })


def filter_category(request):
    if request.method == "GET":
        search_keywords = request.GET['search-keywords']
        category = request.GET['filter-category']
        filtered_listings = get_filtered_listings(search_keywords, category)

        relevant_listings = get_relevant_listings(search_keywords)
        relevant_categories = get_relevant_categories(relevant_listings)

        return render(request, "shopping/search.html", {
            "search_keywords": search_keywords,
            "relevant_listings": filtered_listings,
            "relevant_categories": relevant_categories
        })
    else:
        return search_view(request)


def sort_category(request):
    if request.method == "GET":
        search_keywords = request.GET['search-keywords']
        sort_by = request.GET['sort-category']
        category_filter = request.GET['filter-category']

        if sort_by == "Latest":
            sorted_listings = get_sorted_listings_by_latest(
                search_keywords, category_filter)
        if sort_by == "Price":
            sorted_listings = get_sorted_listings_by_price(
                search_keywords, category_filter)
        if sort_by == "Top Sales":
            sorted_listings = get_sorted_listings_by_sales(
                search_keywords, category_filter)
        if sort_by == "Top Ratings":
            sorted_listings = get_sorted_listings_by_ratings(
                search_keywords, category_filter)

        relevant_listings = get_relevant_listings(search_keywords)
        relevant_categories = get_relevant_categories(relevant_listings)

        return render(request, "shopping/search.html", {
            "search_keywords": search_keywords,
            "relevant_listings": sorted_listings,
            "relevant_categories": relevant_categories
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


def check_listing_review(listing):
    if listing.review.all().count == 0:
        return False
    return True


def update_listing_rating_score(listing):
    total_review_count = Review.objects.filter(listing=listing).count()
    total_score = 0
    for review in Review.objects.filter(listing=listing):
        total_score = total_score + review.rating

    if (total_review_count) == 0:
        listing.rating_score = 0
    else:
        listing.rating_score = total_score / total_review_count
    listing.save()


def parse_rating_score_one_decimal_place(score):
    return ("{:.1f}".format(score))


def check_user_has_reviewed(user, relevant_reviews):
    for review in relevant_reviews:
        if user == review.user:
            return True
    return False


def check_user_has_purchases(user, relevant_orders):
    for order in relevant_orders:
        if user == order.user:
            return True
    return False


def check_user_has_order_in_cart(user):
    if Order.objects.filter(user=user, has_purchased=False).count() == 0:
        return False
    return True


def check_listing_exist_in_cart(listing, user):
    for order in Order.objects.filter(user=user, listing=listing):
        if order.listing == listing:
            return True
    return False


def check_user_has_order_in_cart_exist_in_cart(listing, user):
    for order in Order.objects.filter(user=user, listing=listing):
        if order.listing == listing:
            return True
    return False


def check_user_has_order(user):
    for order in Order.objects.filter(user=user):
        if order.has_purchased is True:
            return False
    return True


def check_user_has_item_sold(user, relevant_orders):
    for order in relevant_orders:
        if order.has_purchased is True:
            return True
    return False


def get_total_price_in_cart(user):
    total_price = 0.00

    for order in Order.objects.filter(user=user, has_purchased=False):
        total_price += (order.quantity_demanded * float(order.listing.price))

    user.order_total_price = total_price
    user.save()
    return total_price


def parse_order_total_price_two_decimal_pace(total_price):
    return ("{0:.2f}".format(total_price))


def update_listing_quantity(orders_in_cart):
    """
    Subtracts quantity_demanded for each order in cart from the respective
    listing quantity. Deletes the order afterwards.
    """
    all_listings = Listing.objects.all()

    for order in orders_in_cart:
        order_quantity_demanded = order.quantity_demanded
        for listing in all_listings:
            if order.listing == listing:
                listing.quantity -= order_quantity_demanded
                if listing.quantity < 0:
                    listing.quantity = 0
                listing.quantity_sold += 1
                listing.save()

        order.has_purchased = True
        order.save()


def check_listing_has_sold_out(listing):
    if listing.quantity == 0:
        return True
    return False


def get_relevant_listings(search_keywords):
    relevant_listings = []
    for listing in Listing.objects.all():
        if search_keywords.lower() in listing.title.lower():
            relevant_listings.append(listing)
    return relevant_listings


def get_relevant_users(search_keywords):
    relevant_users = []
    for user in User.objects.all():
        if search_keywords.lower() in user.username.lower():
            relevant_users.append(user)
    return relevant_users


def get_relevant_categories(relevant_listings):
    relevant_categories = []
    for listing in relevant_listings:
        if listing.category not in relevant_categories:
            relevant_categories.append(listing.category)
    return relevant_categories


def get_filtered_listings(search_keywords, category):
    filtered_listings = []
    for listing in Listing.objects.all().filter(category=category):
        if search_keywords.lower() in listing.title.lower():
            filtered_listings.append(listing)
    return filtered_listings


def get_sorted_listings_by_latest(search_keywords, filter_category):
    sorted_listings = []

    if filter_category == '':
        for listing in Listing.objects.all().order_by('date').reverse():
            if search_keywords.lower() in listing.title.lower():
                sorted_listings.append(listing)
    else:
        for listing in Listing.objects.all().filter(
                category=filter_category).order_by('date'):
            if search_keywords.lower() in listing.title.lower().reverse():
                sorted_listings.append(listing)

    return sorted_listings


def get_sorted_listings_by_price(search_keywords, filter_category):
    sorted_listings = []

    if filter_category == '':
        for listing in Listing.objects.all().order_by('price').reverse():
            if search_keywords.lower() in listing.title.lower():
                sorted_listings.append(listing)
    else:
        for listing in Listing.objects.all().filter(
                category=filter_category).order_by('price').reverse():
            if search_keywords.lower() in listing.title.lower():
                sorted_listings.append(listing)

    return sorted_listings


def get_sorted_listings_by_ratings(search_keywords, filter_category):
    sorted_listings = []

    if filter_category == '':
        for listing in Listing.objects.all().order_by(
                'rating_score').reverse():
            if search_keywords.lower() in listing.title.lower():
                sorted_listings.append(listing)
    else:
        for listing in Listing.objects.all().filter(
                category=filter_category).order_by('rating_score').reverse():
            if search_keywords.lower() in listing.title.lower():
                sorted_listings.append(listing)

    return sorted_listings


def get_sorted_listings_by_sales(search_keywords, filter_category):
    sorted_listings = []

    if filter_category == '':
        for listing in Listing.objects.all().order_by(
                'quantity_sold').reverse():
            if search_keywords.lower() in listing.title.lower():
                sorted_listings.append(listing)
    else:
        for listing in Listing.objects.all().filter(
                category=filter_category).order_by('quantity_sold').reverse():
            if search_keywords.lower() in listing.title.lower():
                sorted_listings.append(listing)

    return sorted_listings
