from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category.name} => {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=150)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(upload_to="product_images", default="default.jpg")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(self, Product).save(*args, **kwargs)

        im = Image.open(self.image)
        width, height = im.size
        
        if width > 300 or height > 300:
            im.thumbnail((300, 300), Image.ANTIALIAS)
            im.save(self.image.path)