from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    product_image = models.ImageField(upload_to='files/images', blank=True, null=True)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='seller')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='winner')

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Watchlist(models.Model):
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    