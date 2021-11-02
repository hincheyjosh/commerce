from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE



class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image_url = models.URLField(default="http://blog.aspneter.com/Images/no-thumb.jpg")
    price = models.FloatField()
    category = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    winning_bid = models.ForeignKey('Bid', on_delete=CASCADE,null=True, blank=True, related_name='+')

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    amount = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"${self.amount:.2f}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)
    content = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.user}, {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)

    def __str__(self):
        return f"{self.user}, {self.listing}"
    
