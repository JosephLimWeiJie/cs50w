
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allpost", views.all_post_view, name="allpost"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("following", views.following_view, name="following"),
    path("editfollower/<str:name>", views.edit_follower, name="editfollower"),

    # API Routes
    path("post/<int:post_id>", views.post, name="post"),
    path("updatelikes/<int:post_id>", views.update_likes, name="updatelikes")
]
