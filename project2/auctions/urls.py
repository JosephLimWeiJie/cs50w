from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("close/<int:listing_id>", views.close_view, name="close"),
    path("comment/<int:listing_id>", views.add_comment_view, name="comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path(
        "addwatchlist/<int:listing_id>", views.add_to_watchlist,
        name="addwatchlist"),
    path(
        "removewatchlist/<int:listing_id>", views.remove_from_watchlist,
        name="removewatchlist"),
    path("category", views.category, name="category"),
    path(
        "categorylisting/<str:category_name>", views.category_listing,
        name="categorylisting")
]
