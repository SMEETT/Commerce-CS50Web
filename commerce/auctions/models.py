from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    imgurl = models.CharField(max_length=128)
    category = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    closed = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentators")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented")
    comment = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.user} said {self.comment} about {self.listing}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidded")
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.listing} Bid: {self.bid}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchers")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")

    def __str__(self):
        return f"{self.user} is watching {self.listing}"