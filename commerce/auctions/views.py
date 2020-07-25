from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .forms import CreateListingForm, BidForm
from .models import User, Category, Listing, Comment, Bid, Watchlist


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        'listings': listings
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            # save the form instance into a new variable, but don't commit to DB
            form_tmp = form.save(commit=False)
            # add the user to the form data
            form_tmp.user = request.user
            # save the form (including current user) to DB
            form_tmp.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/error.html", {
                "error": "Something went wrong :("
            })
        

    elif request.method == "GET":
        # if user is not authenticated, redirect to login
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("auctions:login"))
        # create a form instance, render HTML
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {
            "form": form
        })


def listings(request, listing_id):
    
    listing = Listing.objects.get(id=int(listing_id))
    highest_bid = Bid.objects.all().filter(listing__id=listing_id).order_by("-bid").first()
    bid_form = BidForm()

    return render(request, "auctions/listings.html", {
        "listing": listing,
        "bid_form": bid_form,
        "highest_bid": highest_bid,
    })

def place_bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        listing = Listing.objects.get(id=int(listing_id))

        if form.is_valid():
            form_tmp = form.save(commit=False)
            form_tmp.user = request.user
            form_tmp.listing = listing
            form_tmp.save()
            return redirect('auctions:listings', listing_id=listing_id)

            
            

    elif request.method == "GET":
        return HttpResponseRedirect(reverse("auctions:index"))