from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category_name = models.CharField(max_length=64)

class Products(models.Model):
    name_product = models.CharField(max_length=64) 
    image = models.TextField()
    bid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ProductUser")
    last_user_bid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserBid")
    description = models.TextField()
    category = models.ForeignKey(Categories , on_delete=models.CASCADE, related_name="ProductCategories")
    active = models.BooleanField()

class Watchlist(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="ProductWatch")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserWatch")

class comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ProductCom")
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="UserCom")
    comment = models.TextField()