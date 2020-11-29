from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Cart(models.Model):
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total_price(self):
        total = 0

        for item in self.items.all():
            total += item.total_price

        return total

    def has_product(self, product):
        for item in self.items.all():
            if product.id == item.product.id:
                return True
        
        return False