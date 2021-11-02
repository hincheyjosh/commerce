from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(is_active=True)
    })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing_id)

    if request.user.is_authenticated:
        # Check if current user is owner of listing
        if request.user == listing.user:
            is_user = True
        else:
            is_user = False
        # Check if item in watchlast
        is_watchlist = Watchlist.objects.filter(user=request.user, listing=listing_id)

        if listing.is_active == False:
            message = f'This listing is closed. <strong>{listing.winning_bid.user.username}</strong> has won the auction.'
        else:
            message = None

        return render(request, "auctions/listing.html", {
            'listing': listing,
            'is_user': is_user,
            'is_watchlist': is_watchlist,
            'lowest_bid': listing.price + 0.01,
            'comments': comments,
            'message': message
        })
    else:
        return render(request, "auctions/listing.html", {
            'listing': listing,
            'comments': comments
        })

def categories(request):    
    categories = ['Clothing', 'Toys', 'Musical Instruments', 'Electronics', 'Home',
        'Books', 'Magical Artifacts', 'Other']

    return render(request, "auctions/categories.html", {
        'categories': sorted(categories)
    })

def category(request, category):
    print(category)
    print(category)

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": Listing.objects.filter(is_active=True, category=category)
    })


@login_required(login_url='login')
def addWatchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    new_watchlist = Watchlist(user=user, listing=listing)
    new_watchlist.save()
    return redirect(reverse('listing', kwargs={'listing_id': listing_id}))

@login_required(login_url='login')
def removeWatchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    delete_watchlist = Watchlist.objects.get(user=user,listing=listing)
    delete_watchlist.delete()
    return redirect(reverse('listing', kwargs={'listing_id': listing_id}))

@login_required(login_url='login')
def watchlist(request):
    user = request.user
    listings = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required(login_url='login')
def bid(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    amount = request.POST["bidAmount"]
    if float(amount) <= listing.price:
        return render(request, "auctions/register.html", {
            "message": "Bid is too low."
        })
    new_bid = Bid(amount=amount, listing=listing, user=user)
    new_bid.save()
    listing.price = amount
    listing.save(update_fields=['price'])

    return redirect(reverse('listing', kwargs={'listing_id': listing_id}))

@login_required(login_url='login')
def closeAuction(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    if user == listing.user:
        winning_bid = Bid.objects.get(listing=listing, amount=listing.price)
        listing.winning_bid = winning_bid
        listing.is_active = False
        listing.save(update_fields=['winning_bid','is_active'])
        return redirect(reverse('listing', kwargs={'listing_id': listing_id}))






@login_required(login_url='login')
def create(request):
    categories = ['Clothing', 'Toys', 'Musical Instruments', 'Electronics', 'Home',
    'Books', 'Magical Artifacts', 'Other']

    if request.method == 'POST':
        user = request.user
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        category = request.POST["category"]
        image_url = request.POST["image_url"]

        if image_url == '':
            new_listing = Listing(user=user, title=title, description=description,
            price=price, category=category)
        else:
            new_listing = Listing(user=user, title=title, description=description,
            price=price, image_url=image_url, category=category)

        new_listing.save()

        return redirect(reverse('listing', kwargs={'listing_id': new_listing.id}))

    return render(request, "auctions/create.html", {
        'categories': categories
    })

@login_required(login_url='login')
def comment(request, listing_id):
    user = request.user
    comment = request.POST["comment"]
    listing = Listing.objects.get(id=listing_id)
    new_comment = Comment(user=user, listing=listing, content=comment)
    new_comment.save()
    return redirect(reverse('listing', kwargs={'listing_id': listing_id}))


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
