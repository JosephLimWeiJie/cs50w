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
        "createlisting", views.create_listing_view,
        name="create_listing"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path(
        "updateproductdesrc/<int:listing_id>",
        views.update_listing_desrc_view,
        name="update_product_listing"),
    path("review/<int:listing_id>", views.review_view, name="review"),


    # API Routes
    path(
        "updateprofile/<int:profile_id>", views.update_profile,
        name="updateprofile")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
