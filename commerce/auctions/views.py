from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from decimal import Decimal
from django.views.generic import ListView
from urllib.parse import urlparse
import os.path

from .forms import ListingForm, BidForm, CommentForm
from .models import User, Category, Listing, Comment, Bid, Watchlist

def test(request):
    return render(request, 'auctions/test.html')

def categories(request):
    template = 'auctions/categories.html'
    categories = Category.objects.all()
    categories_id = Listing.objects.order_by().values('category').distinct()
    listings = Listing.objects.all()
    return render(request, template, {
        'categories_id': categories_id,
        'categories': categories,
        'listings': listings,
    })


@login_required
def edit_listing(request, listing_id):
    if request.method == "GET":
        try:
            listing_to_edit = Listing.objects.get(pk=listing_id)
        except:
            return render(request, "auctions/error.html", {
                "error": "404 / Listing doesn't exist."
            })
        if listing_to_edit.user != request.user:
            return render(request, "auctions/error.html", {
                "error": "You can't edit a listing that isn't yours!"
            })
        form = ListingForm(instance=listing_to_edit)
        return render(request, "auctions/edit_listing.html", {
            'form': form,
            'listing': listing_to_edit
        })

    elif request.method == "POST":
        listing_to_update = Listing.objects.get(pk=listing_id)
        form = ListingForm(request.POST or None, instance=listing_to_update)
        if form.is_valid():
            form.save()
            return redirect('auctions:listings', listing_id=listing_id)
        return render(request, 'auctions/edit_listing', {
            'form': form
        })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if not form.is_valid():
            return render(request, "auctions/create_listing.html", {
                "form": form,
            })
        else:
            # save the form instance into a new variable, but don't commit to DB
            form_tmp = form.save(commit=False)
            # add the user to the form data
            form_tmp.user = request.user
            # save the form (including current user) to DB
            form_tmp.save()
            return HttpResponseRedirect(reverse("auctions:index"))

    elif request.method == "GET":
        # if user is not authenticated, redirect to login
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("auctions:login"))
        # create unbound form instance
        form = ListingForm()
        return render(request, "auctions/create_listing.html", {
            "form": form
        })



@login_required
def close_listing(request, listing_id):
    try:
        listing_to_close = Listing.objects.get(pk=listing_id)
    except:
        return render(request, "auctions/error.html", {
                "error": "404 / Listing doesn't exist."
            })
    
    if listing_to_close.user != request.user:
        return render(request, "auctions/error.html", {
                "error": "You can't close a listing that isn't yours!"
            })
    else:
        listing_to_close.closed = True
        listing_to_close.save()
        return redirect('auctions:listings', listing_id=listing_id)

@login_required
def my_listings (request):
    template = "auctions/my_listings.html"
    try:
        my_listings = Listing.objects.filter(user=request.user)
    except:
        my_listings = None
    context = {
        'my_listings': my_listings
    }
    return render(request, template, context)


class IndexList(ListView):
    model = Listing
    template_name = "auctions/index.html"

@login_required
def watchlist(request):
    template = "auctions/watchlist.html"
    watchlist = Watchlist.objects.filter(user=request.user)
    context = {
        'watchlist': watchlist
    }
    return render (request, template, context)

@login_required
def watchlist_toggle(request, listing_id):
    # query listings by listing_id (or render error)
    try:
        listing = Listing.objects.get(id=int(listing_id))
    except:
        return render(request, "auctions/error.html", {
            "error": "404 / Listing doesn't exist."
        })
    try:
        watchlist_entry = Watchlist.objects.all().filter(listing__id=listing_id, user__id=request.user.id)
    except:
        watchlist_entry = None
    if watchlist_entry:
        watchlist_entry.delete()
    else:
        new_watchlist_entry = Watchlist(user=request.user, listing=listing)
        new_watchlist_entry.save()

    # URL Parsing to decide where to redirect
    # Returns the Origin of the Request
    parse = urlparse(request.META['HTTP_REFERER'])
    split = os.path.split(parse.path)

    if split[1] == 'watchlist':
        return redirect('auctions:watchlist')
    else:
        return redirect('auctions:listings', listing_id=listing_id)


@login_required
def listings(request, listing_id):
    # query listings by listing_id (or render error)
    try:
        listing = Listing.objects.get(pk=listing_id)
    except:
        return render(request, "auctions/error.html", {
            "error": "404 / Listing doesn't exist."
        })
    # query for comments or set None
    try:
        comments = Comment.objects.all().filter(listing__id=listing_id)
    except:
        comments = None
    # query for watchlist entry or set None
    try:
        watchlist_entry = Watchlist.objects.all().filter(listing__id=listing_id, user__id=request.user.id)
    except:
        watchlist_entry = None
      
    # unbound form instance
    bid_form = BidForm()  
    comment_form = CommentForm()

    # add everything to a context dictionary
    context = {
    "listing": listing,
    "bid_form": bid_form,
    "comment_form": comment_form,
    "comments": comments,
    "watchlist_entry": watchlist_entry,
    }
    
    if request.method == "POST":
        # check for the form
        if request.POST.get("form_type") == 'place_bid':
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                placed_bid = bid_form.cleaned_data.get('bid_price')
                
                try:
                    highest_bid = Listing.objects.get(pk=listing_id).bids.last().bid_price
                except:
                    highest_bid = 0

                if placed_bid <= highest_bid or placed_bid <= listing.start_price:
                    bid_form.add_error("bid_price", "Your bid is too low :(")
                    context["bid_form"] = bid_form
                    return render(request, "auctions/listings.html", context)

                # add placed_bid to Listing
                listing_to_update = Listing.objects.get(pk=listing_id)
                bid_to_add = Bid(user=request.user, bid_price=placed_bid)
                bid_to_add.save()
                listing_to_update.bids.add(bid_to_add)

                return redirect('auctions:listings', listing_id=listing_id)
        
        elif request.POST.get("form_type") == "post_comment":
                comment_form = CommentForm(request.POST)

                # TODO Check for comment length!

                if comment_form.is_valid():
                    form_tmp = comment_form.save(commit=False)
                    form_tmp.user = request.user
                    form_tmp.listing = listing
                    form_tmp.save()
                    return redirect('auctions:listings', listing_id=listing_id)

    elif request.method == "GET":
        return render(request, "auctions/listings.html", context)


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