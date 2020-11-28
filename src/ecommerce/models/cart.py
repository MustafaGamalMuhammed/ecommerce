from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import Product


class Cart(models.Model):
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total_price(self):
        total = 0

        for product in self.products.all():
            total += product.price

        return total