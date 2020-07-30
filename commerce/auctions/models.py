from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
    imgurl = models.CharField(max_length=128)
    start_price = models.DecimalField(max_digits=12, decimal_places=2)
    closed = models.BooleanField(default=False, editable=False)

    bids = models.ManyToManyField('Bid', blank=True, related_name='listing_bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=12, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} ({self.bid_price}) @ {self.listing}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentators")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented")
    comment = models.CharField(max_length=1024)
    date_created = models.DateField(blank=True, null=True, editable=False, auto_now_add=True)

    def __str__(self):
        return f"{self.user}: '{self.comment}' ({self.listing})"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchers")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")

    def __str__(self):
        return f"{self.user} is watching ''{self.listing}''"
