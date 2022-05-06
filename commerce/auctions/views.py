
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Auction, Bid, Comment, Watchlist, Category, User

class CreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    image = forms.CharField(widget=forms.URLInput())
    start_bid = forms.CharField(widget=forms.NumberInput())
    category = forms.SelectMultiple()


class BidForm(forms.Form):
    bid = forms.DecimalField()


class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment")


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all().filter(active=True)
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
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all(),
            "form": CreateForm()
        })
    else:
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            start_bid = form.cleaned_data["start_bid"]
            image = form.cleaned_data["image"]
            description = form.cleaned_data["description"]
            user = request.user
            category = Category.objects.get(id=request.POST["categories"])
            auction = Auction.objects.create(user = user, title = title, description = description, 
            start_bid = start_bid, image = image, category = category)  
            auction.save() 

            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html", {
            "categories": Category.objects.all(),
            "form": CreateForm(request.POST)
        })


@login_required
def listing(request, auction_id):
    user = request.user
    auction = Auction.objects.get(pk=auction_id)
    current_bid = Bid.objects.filter(auction=auction).order_by('value').last()
    if request.method == 'GET':
        if auction.active == False:
            winner = Bid.objects.filter(auction=auction).order_by('value').last()
            if winner.user_id == user.id:
                return render(request, "auctions/listing.html", {
                    "winner": winner
                })
        if user == auction.user:
            owner = True
            return render(request, "auctions/listing.html", {
            "auction": auction,
            "form": BidForm(),
            'current_bid':current_bid,
            'owner': owner })
        else:
            return render(request, "auctions/listing.html", {
            "auction": auction,
            "form": BidForm(),
            "comments": Comment.objects.filter(auction=auction),
            "cform": CommentForm(),
            'current_bid':current_bid })


    else:
        cform = CommentForm(request.POST)
        auction = Auction.objects.get(pk=auction_id)
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            user = request.user

            if bid < auction.start_bid:
                return render(request, "auctions/error.html", {
                "error1": "bid must be more than starting bid"
            })

            if bid < current_bid.value and bid > auction.start_bid:
                return render(request, "auctions/error.html", {
                "error2": "bid must be more than current bid"
            }) 
           
            Bid.objects.create(value=bid, user=user, auction=auction)

        if cform.is_valid():
            comment = cform.cleaned_data['comment']
            user = request.user

            Comment.objects.create(user=user, comment=comment, auction=auction)

            return HttpResponseRedirect('/listing/%i' %auction.id)


@login_required
def close(request, auction_id):
    auction = auction = Auction.objects.get(pk=auction_id)
    print(auction)
    user = request.user
    auction.active = False
    auction.save()
    

    return HttpResponseRedirect(reverse('index'))


@login_required
def comment(request, auction_id):
    auction = auction = Auction.objects.get(pk=auction_id)
    user = request.user
    form = CommentForm(request.POST)
    if form.is_valid:
        comment = form.cleaned_data["comment"]

        return render(request, "listing/<int:auction_id>", {
            'formcomment':CommentForm()
        })


def categories(request):
    auctions = []    
    if request.method == "POST":
        category = request.POST["categories"]
        auctions = Auction.objects.filter(category = category)

    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "auctions": auctions
    })


def toggle_watchlist(request, listing_id):
    
    user = request.user
    l = Auction.objects.filter(id = listing_id).first()
    
    w = Watchlist.objects.filter(user = user, listing = l).first()
    
    if w is None:
        wl = Watchlist.objects.create(user = user,
                                      listing = l)
        wl.save()
        return HttpResponseRedirect(reverse("watchlist"))
    
    w.delete()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist(request):
    
    user = request.user
    wl = Watchlist.objects.filter(user = user)
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": wl
    })








    
