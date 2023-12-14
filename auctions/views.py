from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms

from .models import User, Listing
import datetime
from django.contrib.auth.decorators import login_required

class UploadImage(ModelForm):
    class Meta:
        model = Listing
        fields = ['product_name', 'description', 'starting_bid', 'product_image']
        labels = {
            "description": "",
            "starting_bid": "",
            "product_name": "",
            "product_image": "",
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder': "Enter description here...",
                'rows':"4" 
                }),
            'starting_bid': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': "Starting Bid",
                'min':"0"
                }),
            'product_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Title"
                }),
            'product_image': forms.FileInput(attrs={
                'style': "display: none;",
                }),
            
        }



def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
        if request.POST:
            frm = UploadImage(request.POST, request.FILES)
            if frm.is_valid():
                newlisting = frm.save(commit=False)
                newlisting.seller = request.user
                newlisting.date_created = datetime.datetime.now()
                newlisting.save()
        return render(request, "auctions/create.html", {'form': UploadImage()})


@login_required
def listing(request, listing_id):
    lst = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": lst
    })