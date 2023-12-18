from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms

from .models import User, Listing, Watchlist, Bid
import datetime
from django.contrib.auth.decorators import login_required


class Create_Listing(ModelForm):
    class Meta:
        model = Listing
        fields = ['product_name', 'description', 'price', 'product_image']
        labels = {
            "description": "",
            "price": "",
            "product_name": "",
            "product_image": "",
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder': "Enter description here...",
                'rows':"4" 
                }),
            'price': forms.NumberInput(attrs={
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


class Place_Bid(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            "amount": "",
        }
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': "Bid",
                'min':"0",
                'max':"99999999",
                'style':"margin-top:20px;"
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
            frm = Create_Listing(request.POST, request.FILES)
            if frm.is_valid():
                newlisting = frm.save(commit=False)
                newlisting.seller = request.user
                newlisting.date_created = datetime.datetime.now()
                newlisting.save()
        return render(request, "auctions/create.html", {'form': Create_Listing()})


def listing(request, listing_id):
    prd = Listing.objects.get(pk=listing_id)
    if Watchlist.objects.filter(product=prd, user=request.user):
        is_w = True
    else:
        is_w = False
    lst = Listing.objects.get(id=listing_id)
    if request.POST:
        bid = float(request.POST.get('amount'))
        frm = Place_Bid(request.POST)
        prd = Listing.objects.get(pk=listing_id)
        count_bid = Bid.objects.filter(product=prd).count()
        redirect_url = reverse('listing', args=[listing_id]) 
        if frm.is_valid():
            if (count_bid == 0 and bid >= prd.price) or (count_bid > 0 and bid > prd.price):
                new_bid = frm.save(commit=False)
                new_bid.bidder = request.user
                new_bid.product = prd
                new_bid.save()
                new_p = Listing.objects.get(pk=listing_id)
                new_p.price = bid
                new_p.save()
                lst = Listing.objects.get(id=listing_id)        
                return render(request, "auctions/listing.html", {
                    'form': Place_Bid(),
                    "listing": lst,
                    "is_whatchlist":is_w
        })
            else:
                return render(request, "auctions/listing.html", {
                        'form': Place_Bid(),
                        "listing": lst,
                        "is_whatchlist":is_w,
                        'message':'The amount you offer is low.'
            })

    return render(request, "auctions/listing.html", {
        'form': Place_Bid(),
        "listing": lst,
        "is_whatchlist":is_w
    })

@login_required
def watchlist(request, listing_id):
    prd = Listing.objects.get(pk=listing_id)   
    redirect_url = reverse('listing', args=[listing_id])

    if Watchlist.objects.filter(product=prd, user=request.user):
        Watchlist.objects.filter(product=prd,user=request.user).delete()
        return HttpResponseRedirect(redirect_url)
    wtchl = Watchlist(product= prd, user = request.user)
    wtchl.save()
    return HttpResponseRedirect(redirect_url)
   
@login_required
def close_bid(request, listing_id):
    lst = Listing.objects.get(pk=listing_id)
    prc = lst.price
    h_bid = Bid.objects.get(amount=prc, product=lst).bidder
    print(h_bid)
    wnr = h_bid
    lst.winner = wnr
    lst.save()
    redirect_url = reverse('listing', args=[listing_id])
    return HttpResponseRedirect(redirect_url)

    '''
    if request.POST:
            bid = float(request.POST.get('amount'))
            frm = Place_Bid(request.POST)
            prd = Listing.objects.get(pk=listing_id)
            count_bid = Bid.objects.filter(product=prd).count()
            redirect_url = reverse('listing', args=[listing_id]) 
            if frm.is_valid():
                if (count_bid == 0 and bid >= prd.price) or (count_bid > 0 and bid > prd.price):
                    new_bid = frm.save(commit=False)
                    new_bid.bidder = request.user
                    new_bid.product = prd
                    new_bid.save()
                    new_p = Listing.objects.get(pk=listing_id)
                    new_p.price = bid
                    new_p.save()


            return HttpResponseRedirect(redirect_url)
'''


