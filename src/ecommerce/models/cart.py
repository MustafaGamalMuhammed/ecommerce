from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Cart"
