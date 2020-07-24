from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .forms import CreateListingForm
from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html")


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
        

    elif request.method == "GET":
        # if user is not authenticated, redirect to login
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("auctions:login"))
        # create a form instance, render HTML
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {
            "form": form
        })