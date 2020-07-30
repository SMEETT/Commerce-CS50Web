from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.IndexList.as_view() , name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_toggle/<int:listing_id>", views.watchlist_toggle, name="watchlist_toggle"),
    path("test", views.test , name="test"),
]