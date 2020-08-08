from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like, Follower


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all_post_view(request):
    if request.method == "POST":
        content = request.POST["content"]

        post = Post.objects.create(user=request.user, content=content)
        like = Like.objects.create(post=post)
        post.save()
        like.save()

        post_list = Post.objects.all().order_by("datetime").reverse()
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/allpost.html", {
            "page_obj": page_obj,
            "posts": post_list,
            "likes": Like.objects.all()
        })
    else:
        post_list = Post.objects.all().order_by("datetime").reverse()
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/allpost.html", {
            "page_obj": page_obj,
            "posts": post_list,
            "likes": Like.objects.all()
        })


def profile(request, name):
    if request.user.username == name:
        post_list = Post.objects.all().filter(
            user=request.user).order_by("datetime").reverse()
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/profile.html", {
            "num_follower": request.user.follower_count,
            "num_following": request.user.following_count,
            "is_not_user": False,
            "user_name": request.user,
            "posts": Post.objects.all().filter(
                user=request.user).order_by("datetime").reverse(),
            "page_obj": page_obj,
            "post_list": post_list
        })
    else:
        # Load other user's profile
        other_user = User.objects.get(username=name)
        curr_session_user = request.user

        post_list = Post.objects.all().filter(
            user=other_user).order_by("datetime").reverse(),
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/profile.html", {
            "num_follower": other_user.follower_count,
            "num_following": other_user.following_count,
            "is_not_user": True,
            "is_following_user": is_following_user(
                curr_session_user, other_user),
            "user_name": other_user,
            "page_obj": page_obj,
            "post_list": Post.objects.all().filter(
                user=other_user).order_by("datetime").reverse()
        })


def following_view(request):

    post_list = Post.objects.all().exclude(
        user=request.user).order_by("datetime").reverse()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "likes": Like.objects.all(),
        "curr_session_user_followings": parse_user_followings(
            request.user.following),
        "page_obj": page_obj,
        "post_list": Post.objects.all().exclude(
            user=request.user).order_by("datetime").reverse()
    })


def edit_follower(request, name):
    if request.method == "POST":
        user = User.objects.get(username=name)
        curr_session_user = request.user

        # Add follower
        if request.POST["edit_follow_button"] == "Follow":
            user.follower_count += 1
            curr_session_user.following_count += 1
            follower = Follower.objects.create(
                name=request.user.username, following=user)
            curr_session_user.following = add_following_into_followings(
                curr_session_user.following, user.username)

            user.save()
            curr_session_user.save()
            follower.save()
        # Remove follower
        else:
            user.follower_count -= 1
            curr_session_user.following_count -= 1
            follower = Follower.objects.get(
                name=curr_session_user.username, following=user)
            follower.delete()
            curr_session_user.following = remove_following_into_followings(
                curr_session_user.following, user.username)

            user.save()
            curr_session_user.save()

        return HttpResponseRedirect(reverse('profile', args=[name]))


""" Utility functions """


def get_num_of_followings(name):
    followers_count = 0
    for follower in Follower.objects.all():
        if follower.user == name:
            followers_count += 1

    return followers_count


def is_following_user(curr_session_user, other_user):
    is_following = False
    for follower in other_user.follower.all():
        if follower.name == curr_session_user.username:
            return True

    return is_following


def add_following_into_followings(
        curr_session_user_followings, following_to_add):

    return curr_session_user_followings + following_to_add + ","


def remove_following_into_followings(
        curr_session_user_followings, following_to_delete):

    if curr_session_user_followings is None:
        return ""
    else:
        following_users = curr_session_user_followings.split(",")
        updated_session_user_followings = ""
        for i in range(0, len(following_users) - 1):
            updated_session_user_followings + following_users[i] + ","

        return updated_session_user_followings


def parse_user_followings(user_followings):
    if user_followings is None:
        return ""
    else:
        return user_followings.split(",")
