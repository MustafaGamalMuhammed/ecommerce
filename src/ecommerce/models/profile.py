from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import Cart, Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    likes = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s profile"