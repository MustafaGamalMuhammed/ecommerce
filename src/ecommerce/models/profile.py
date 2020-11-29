from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from .cart import Cart
from .product import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    likes = models.ManyToManyField(Product)
    products = models.ManyToManyField(Product, related_name="seller")

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('profile', args=(self.id,))