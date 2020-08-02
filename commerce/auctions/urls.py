from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.IndexList.as_view() , name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("edit_listing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("delete_listing/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_toggle/<int:listing_id>", views.watchlist_toggle, name="watchlist_toggle"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("categories", views.categories, name="categories")
]