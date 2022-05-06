from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{ self.name }"

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(blank=False, default=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    category = models.ForeignKey(Category,blank=True, on_delete=models.PROTECT, related_name="categories")
    start_bid = models.FloatField()
    image = models.URLField(blank=True, null=True)
    winner = models.ForeignKey(User, blank=True, on_delete = models.CASCADE, related_name="auction_winner", null=True)

    def __str__(self):
        return f"{self.title} {self.description} {self.start_bid} {self.category}"        

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    value = models.FloatField()
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.value}" 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    listing = models.ForeignKey(Auction, on_delete = models.CASCADE, blank = False)
