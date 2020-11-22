from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_most_sold_products(self):
        products = []

        for subcategory in self.subcategories.all():
            products.extend(subcategory.get_most_sold_products())

        return products


class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.category.name} => {self.name}"

    def get_most_sold_products(self):
        products = self.products.order_by('-sold')[:15]
        return list(products)


class Product(models.Model):
    name = models.CharField(max_length=150)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(upload_to="product_images", default="default.jpg")
    available = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(self, Product).save(*args, **kwargs)

        im = Image.open(self.image)
        width, height = im.size
        
        if width > 300 or height > 300:
            im.thumbnail((300, 300), Image.ANTIALIAS)
            im.save(self.image.path)