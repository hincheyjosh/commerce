from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "category", "price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "amount")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)