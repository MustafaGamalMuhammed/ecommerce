from django.shortcuts import reverse
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from decimal import Decimal
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_most_sold_products(self):
        products = None

        for subcategory in self.subcategories.all():
            if products == None:
                products = subcategory.get_most_sold_products()
            else:
                products = (products | subcategory.get_most_sold_products())

        if products:
            return products.order_by('-sold')[:5]
        else:
            return []

class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.category.name} => {self.name}"

    def get_absolute_url(self):
        return reverse("shop") + f"?subcategory__name={self.name}"

    def get_most_sold_products(self):
        products = self.products.order_by('-sold')
        return products


class Product(models.Model):
    name = models.CharField(max_length=150)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(upload_to="product_images", default="default.jpg")
    available = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', args=(self.id,))

    @property
    def rating(self):
        result = 0

        for review in self.reviews.all():
            result += review.rating

        if result:
            return result / self.reviews.count()
        else:
            return 0

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        im = Image.open(self.image)
        width, height = im.size
        
        if width > 300 or height > 300:
            im.thumbnail((300, 300), Image.ANTIALIAS)
            im.save(self.image.path)


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s review, {self.content[:30]}..."
