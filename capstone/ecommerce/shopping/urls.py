from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:name>", views.profile_view, name="profile"),
    path(
        "updateprofilepic", views.update_profile_pic,
        name="update_profile_pic"),
    path(
        "updateprofileaddr", views.update_profile_delivery_addr,
        name="update_profile_delivery_addr"),
    path(
        "createlisting", views.create_listing_view,
        name="create_listing"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path(
        "updateproductdesrc/<int:listing_id>",
        views.update_listing_desrc_view,
        name="update_product_listing"),
    path("review/<int:listing_id>", views.review_view, name="review"),
    path(
        "updatereview/<int:listing_id>", views.update_review_view,
        name="update_review"),
    path("category/<str:category_name>", views.category_view, name="category"),
    path("categorysort", views.category_sort_view, name="categorysort"),
    path("cart", views.cart_view, name="cart"),
    path("updatecart", views.update_cart_view, name="updatecart"),
    path("checkout", views.checkout_view, name="checkout"),
    path("trackorder/<str:name>", views.track_order_view, name="trackorder"),
    path("receiveorder", views.receive_order, name="receive_order"),

    # API Routes
    path(
        "updateprofile/<int:profile_id>", views.update_profile,
        name="updateprofile"),
    path(
        "updateorder/<int:order_id>", views.update_order,
        name="updateorder"),
    path(
        "updatelisting/<int:listing_id>", views.update_listing,
        name="updatelisting"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
