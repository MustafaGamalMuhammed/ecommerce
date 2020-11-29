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
    seller = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="products")
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

    def get_data(self, request):
        d = {}
        d['id'] = self.id
        d['name'] = self.name
        d['rating'] = self.rating
        d['price'] = self.price
        d['image'] = self.image.url
        d['available'] = self.available
        d['url'] = self.get_absolute_url()
        d['description'] = self.description
        d['seller_name'] = self.seller.user.username
        d['seller_url'] = self.seller.get_absolute_url()
        d['is_authenticated'] = request.user.is_authenticated

        if request.user.is_authenticated:
            d['is_liked'] = self in request.user.profile.likes.all()
            d['is_in_cart'] = request.user.profile.cart.has_product(self)
        
        d['reviews'] = []

        for review in self.reviews.all():
            r = review.get_data()    
            d['reviews'].append(r)

        return d

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

    def get_data(self):
        d = {}
        d['id'] = self.id
        d['username'] = self.user.username
        d['rating'] = self.rating
        d['content'] = self.content

        return d

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, null=True, on_delete=models.SET_NULL, related_name="profile")
    likes = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('profile', args=(self.id,))
